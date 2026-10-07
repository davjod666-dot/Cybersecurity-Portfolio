#!/usr/bin/env python3
"""Alert on received UFW BLOCK TCP/UDP records; never changes firewall policy."""
import collections
import ipaddress
import json
import logging
import shutil
import subprocess
import time

WINDOW = 60.0
COOLDOWN = 600.0
MAX_SOURCES = 4096


def parse(message):
    if '[UFW BLOCK] ' not in message:
        return None
    fields = dict(item.split('=', 1) for item in message.split() if '=' in item)
    if not fields.get('IN') or fields.get('OUT') or fields.get('PROTO') not in ('TCP', 'UDP'):
        return None
    try:
        source = ipaddress.ip_address(fields['SRC'])
        port = int(fields['DPT'])
    except (KeyError, ValueError):
        return None
    if source.is_unspecified or source.is_multicast or not 1 <= port <= 65535:
        return None
    return str(source), (fields['PROTO'], port)


class Detector:
    def __init__(self):
        self.sources = collections.OrderedDict()

    def feed(self, source, pair, now):
        # Expire quiet sources only after cooldown and window have both elapsed.
        for key, state in list(self.sources.items()):
            if now - state['seen'] >= COOLDOWN:
                del self.sources[key]
        if source not in self.sources:
            if len(self.sources) >= MAX_SOURCES:
                self.sources.popitem(last=False)
                logging.warning('Source-state capacity reached; evicted oldest source')
            self.sources[source] = {'events': collections.deque(), 'alert': None, 'seen': now}
        state = self.sources[source]
        state['seen'] = now
        self.sources.move_to_end(source)
        events = state['events']
        while events and now - events[0][0] >= WINDOW:
            events.popleft()
        events.append((now, pair))
        # 30 newest events suffice for the attempts branch; all earlier pairs
        # can be discarded once attempts reaches 30. This bounds memory.
        while len(events) > 30:
            events.popleft()
        count = len(events)
        distinct = len({event[1] for event in events})
        eligible = state['alert'] is None or now - state['alert'] >= COOLDOWN
        if eligible and (count >= 30 or distinct >= 8):
            state['alert'] = now
            return {'source': source, 'attempts': count, 'pairs': distinct}
        return None


def notify(alert):
    body = (f"Source {alert['source']}: {alert['attempts']} logged attempts, "
            f"{alert['pairs']} protocol/port pairs in the last 60 seconds. "
            'Log-based coverage only; traffic was already blocked.')
    logging.warning('SCAN ALERT: %s', body)
    tool = shutil.which('notify-send')
    if tool:
        try:
            result = subprocess.run([tool, '-a', 'UFW scan watcher', '-u', 'normal',
                                     'Blocked probe burst', body], timeout=5,
                                    capture_output=True, text=True)
            if result.returncode:
                logging.error('Desktop notification failed: %s', result.stderr.strip())
        except (OSError, subprocess.TimeoutExpired) as exc:
            logging.error('Desktop notification failed: %s', exc)
    else:
        logging.error('notify-send unavailable; alert recorded in service journal only')


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    detector = Detector()
    logging.info('Started: 60s rolling window (age <60); 8 pairs OR 30 records; '
                 '600s per-source cooldown (elapsed >=600). State resets on restart.')
    # Start at the current tail; no historic events or synthetic production logs.
    command = ['journalctl', '-k', '-f', '-n', '0', '-o', 'json', '--no-pager']
    child = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    try:
        for line in child.stdout:
            try:
                record = json.loads(line)
                message = record.get('MESSAGE', '')
                parsed = parse(message) if isinstance(message, str) else None
            except (ValueError, TypeError):
                logging.warning('Malformed journal record skipped')
                continue
            if parsed:
                alert = detector.feed(*parsed, time.monotonic())
                if alert:
                    notify(alert)
        raise RuntimeError(f'Kernel journal stream ended (exit {child.wait()})')
    finally:
        child.terminate()
        try:
            child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()


if __name__ == '__main__':
    main()
