# Replacement UFW scan watcher — 7 October 2026

New implementation; the original script was not recovered. No firewall changes are made.

Run `bash install.sh` from the saved bundle as your normal desktop user (not with sudo). It reruns tests, checks kernel journal access, backs up any existing matching files, installs a user service, enables it, and sends an explicitly labelled notification check. Confirm the service remains active and the notification appears. Installation cannot be confirmed from this restricted agent session because the user systemd bus is inaccessible.

## Behaviour

Reads new current-boot kernel journal records using `journalctl -k -f -n 0 -o json`. Only inbound `[UFW BLOCK]` TCP/UDP records with valid source and destination port count. One record is one attempt; it is not deduplicated into connection attempts. Separate source state; protocol/port pairs count as distinct. IPv4 and IPv6 source addresses parse, though IPv6 is disabled on this workstation.

Alerts at eight distinct pairs OR thirty records within a rolling window. Ages exactly 60 seconds expire. Cooldown expires at elapsed 600 seconds, measured from the last alert decision. Suppressed events still count within the current window but do not extend cooldown; a new qualifying input is required to alert again. Delivery-time monotonic clock avoids wall-clock jumps; ingestion delay/backlogs can distort relation to actual packet timing. Restart clears all counting/cooldown state and skips historic records. State is bounded to 4096 sources and 30 newest records per source; source eviction can weaken cooldown/coverage under unusually high source churn.

Alerts go to the service journal and `notify-send`. Failed desktop delivery is logged; cooldown still starts from the alert decision, with no delivery retries. Desktop/user-service activation is tied to the user's session, not guaranteed before login. No automatic bans or access-policy changes occur.

## Verification and limits

Ten deterministic offline tests passed using the exact parser/detector code: 29/30/31 attempts; eight pairs; source isolation/per-source cooldown; 59.999/60/60.001 expiry; carry-over; 599.999/600/600.001 cooldown; suppressed events not extending cooldown; stale events not alerting; bounded storage; parser filtering. These tests do not inject fake production logs or send network traffic.

Owner-supplied installer output confirms service enablement/active status, and a journal read confirms Python startup. The owner confirmed a standalone notification appeared. Live detector-to-notification integration, service restart/login/reboot and network-to-alert behaviour remain unverified. Current UFW block logs were captured as rate-limited to three/minute, burst ten. Thirty packets in sixty seconds cannot be assumed to produce thirty records. The thirty-record branch is verified offline only; the watcher can miss slow probes, rate-limited events, accepted traffic and traffic stopped at the router. A notification check tests notification presentation only, not the detector or firewall path.

Status commands:

```sh
systemctl --user status ufw-scan-watcher.service --no-pager
journalctl --user -u ufw-scan-watcher.service -n 20 --no-pager
```

Disable without changing firewall policy:

```sh
systemctl --user disable --now ufw-scan-watcher.service
```

References: [journalctl documentation](https://www.freedesktop.org/software/systemd/man/255/journalctl.html), [desktop notification specification](https://specifications.freedesktop.org/notification/latest/).
