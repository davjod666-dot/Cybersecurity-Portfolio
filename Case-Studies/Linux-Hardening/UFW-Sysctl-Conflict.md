# Linux Host Hardening: UFW and sysctl Configuration Conflict

**Analyst:** David Seabrook

**Date:** 1 October 2026

**Environment:** Personal Omarchy Linux workstation

**Scope:** Historical 1 October assessment: AI-assisted configuration review, implementation, and isolated validation. Current replacement-installation results are recorded separately below.

**Contribution:** I defined the workstation requirements and requested the hardening changes. Codex assisted with configuration and code inspection, implementation, and test execution. This case records that assisted work.

## Question

Would custom ping suppression remain consistent when UFW reloaded its own kernel settings?

## Finding

Two sources assigned different values to the same setting:

```ini
# Custom configuration under /etc/sysctl.d/
net.ipv4.icmp_echo_ignore_all = 1

# Existing /etc/ufw/sysctl.conf
net/ipv4/icmp_echo_ignore_all=0
```

Dots and slashes identify the same sysctl key. A value of `1` suppresses ICMP Echo Replies; `0` permits normal kernel echo handling.

Inspection of the installed `/usr/lib/ufw/ufw-init-functions` showed that `ufw_reload()` invokes `ufw_start()`. Startup loads the file identified by `IPT_SYSCTL`, which pointed to `/etc/ufw/sysctl.conf` on this workstation. This identifies a code path through which UFW can apply its configured sysctl value during reload; it does not establish that a pre-fix reload was observed resetting the live value.

The conflicting configuration values and installed reload code were inspected. The pre-fix reset was not deliberately reproduced, and this case does not present a captured pre-fix failure. No clean-install reproduction is documented.

## Change

- Aligned both configuration sources to `icmp_echo_ignore_all=1`.
- Retained a firewall DROP rule for inbound ICMP Echo Requests.
- Retained firewall rules intended to allow useful ICMP error handling and replies to outbound connections; the documented validation does not establish that all of those behaviours were tested.
- Backed up configuration and recorded live values before broader sysctl hardening.

The retained firewall rule is configured to drop inbound ICMP Echo Requests without responding. Separately, `icmp_echo_ignore_all=1` is configured to suppress IPv4 Echo Replies if requests reach the kernel echo handler. The recorded no-reply ping result does not establish each control’s effectiveness independently.

## Recorded post-change validation

The table summarises results recorded during the AI-assisted session after the changes. The checks demonstrate only the settings and behaviours exercised at that time. They do not reproduce the pre-fix reset or establish persistence across reboot.

| Check | Result |
| --- | --- |
| Kernel value after UFW reload | `net.ipv4.icmp_echo_ignore_all = 1` |
| Ping from an isolated temporary network | No replies |
| Eight blocked TCP destination ports from the test source | Scan detector generated an alert |
| DNS query after hardening | Successfully resolved |
| Firewall and desktop monitor | Active |
| Sysctl hardening settings after UFW reload | All 35 configured entries were recorded as matching the intended live values after UFW reload, including per-interface values; this was a value check, not a behavioural test of every setting. |

The temporary network was removed after testing. The watcher was configured with a 60-second window, an alert threshold of eight distinct blocked protocol/port pairs or 30 attempts from one source, and a ten-minute per-source cooldown. The recorded test generated an alert using eight blocked TCP destination ports; separate tests of the 30-attempt threshold, window boundaries, and cooldown are not documented.

## Limits

- This is a configuration conflict, not a finding that normal ping replies are a vulnerability.
- A clean-install reproduction has not established an Omarchy-specific bug.
- Ping suppression does not conceal allowed services.
- The scan watcher cannot see traffic blocked by the router; slow scans and logging-rate limits reduce coverage.
- Boot persistence is configured but was not tested by rebooting.
- The validation table summarises recorded session results; full raw output is not published here. The read-only commands below are later verification guidance, not preserved commands or output from that session.

## Control-assurance lesson

Configuration files are evidence of intended policy. Read-back checks and controlled tests provide evidence of current behaviour. Check all services that can apply the same kernel setting, then validate after they reload.

## Read-only checks for the current configuration

On a workstation with the same file layout, these read-only commands report the live ping setting and locate matching text in selected configuration files and the installed UFW code. The code matches are starting points for reading the surrounding functions; they do not themselves demonstrate execution of the reload path.

```sh
sysctl net.ipv4.icmp_echo_ignore_all
rg -n 'icmp_echo_ignore_all' /etc/sysctl.d/ /etc/ufw/sysctl.conf
rg -n 'ufw_reload|ufw_start|IPT_SYSCTL|sysctl' /usr/lib/ufw/ufw-init-functions /etc/default/ufw
```

The intended policy is that both configuration sources assign `1` and the live value is `1`. These commands are a verification guide, not a preserved transcript of the original test. They do not perform a UFW reload, reproduce the isolated network tests, check all 35 hardening entries, or establish reboot persistence. Matching values show agreement at the time of inspection, not which component last applied them.

## Follow-up evidence — 6–7 October 2026

The sections above describe the 1 October assessment. This follow-up reviews commit `7592f7d` and records subsequent work on a replacement installation. Workstation evidence came from owner-supplied terminal output and manually reported Windows results; full raw workstation transcripts and packet captures are not published here. Offline replacement-watcher tests were run against the published code. No framework compliance claim is made.

### Reinstall and restoration

The owner confirmed a crash and reinstall after the original assessment; package history records Omarchy, NetworkManager and UFW installation on 4 October. This explains why historical checks cannot establish the replacement installation's policy; the discrepancies are not attributed to unauthorised alteration.

Before restoration, the live ping value and UFW sysctl assignment were `0`, no matching custom assignment was found in the searched sysctl directories, and the effective firewall and `/etc/ufw/before.rules` allowed IPv4 Echo Requests. IPv6 all/default disable flags were `0`; the wired profile used `auto` and the interface had a link-local IPv6 address/route. No global IPv6 address or default route appeared in that capture.

The owner then aligned the UFW and custom sysctl ping assignments to `1`, restored the INPUT Echo Request DROP in `before.rules`, added persistent IPv6 all/default disable assignments, and saved the wired profile with IPv6 method `disabled` after clearing its IPv6 DNS entries. Reload output and live read-backs confirmed the ping setting and DROP rule.

### V1: observed reboot persistence

| Capture (UTC, 6 October) | Boot ID | Recorded state |
| --- | --- | --- |
| 11:42:29, before reboot | `77449a3c-2ac4-4661-8619-ea651cddb16b` | Ping value `1`; IPv6 all/default disable flags `1`; profile `disabled`; active UFW; IPv4 Echo Request DROP loaded; no IPv6 addresses/routes shown |
| 11:54:04, after reboot | `d6440baf-efc0-4874-a892-89af63d59117` | Same inspected settings, rule and service state; no IPv6 addresses/routes shown |

**Result:** these restored settings persisted across one reboot. An earlier reboot also retained the ping value `1` and active UFW, before the DROP restoration. Boot journal output showed kernel-variable and UFW startup completion. These are setting/rule checks, not verification of all 35 historical entries, startup attribution for each key, future updates or every packet path.

### V2: LAN ping observations

The Windows 11 EliteBook and workstation were on the same local subnet. These tests used the actual replacement workstation, with temporary INPUT exceptions scoped to the peer, destination, wired interface and IPv4 Echo Requests; the proposed disposable-clone matrix below was not executed in full.

| Check | Supplied evidence | Supported conclusion / limit |
| --- | --- | --- |
| Firewall DROP | Owner reported four ping timeouts; successive Echo Request DROP counters increased from 4 packets/240 bytes to 8 packets/480 bytes | Four additional requests were dropped. The counter is aggregate; peer attribution relies on the reported sequence, without packet capture. |
| Kernel suppression with scoped firewall passage | A temporary first-position ACCEPT counted four requests/240 bytes from the peer; owner affirmed Windows timeouts; subsequent kernel read-back was `1` | Supports kernel suppression on this path. Initial live-value/counter captures during the burst were not supplied. |
| Positive reply control | Script output shows temporary kernel value `0`; owner reported four replies (32 bytes, approximately 3 ms, TTL 64) during equivalent scoped passage | Demonstrates the peer could receive replies when suppression was off. Windows output was manually reported. |
| Cleanup | Script restored `1`; live read-back confirmed `1`; INPUT listing contained neither temporary exception | Intended protection restored. |

**Result:** firewall dropping and kernel suppression are supported separately on the observed path, with the attribution/capture limits above. The complete matrix, including a firewall-only row with kernel suppression deliberately off and repeated positive/negative alternation, remains unexecuted. Useful ICMP error behaviour and IPv6 packet behaviour were not tested.

### V3: replacement scan watcher

A limited search did not recover the historical watcher. A [new implementation](../../Tools-And-Methods/UFW-Scan-Watcher/README.md) was built and installed, rather than claiming the old script was restored. It reads existing inbound `[UFW BLOCK]` TCP/UDP records and alerts at eight distinct protocol/port pairs OR thirty records in a rolling 60-second window, with a 600-second per-source cooldown. Event ages exactly 60 seconds expire; cooldown eligibility begins at elapsed 600 seconds. It uses monotonic delivery time, resets state on restart, and does not change firewall rules.

Ten offline tests of the actual parser/detector passed: 29/30/31 attempts, distinct pairs, source isolation, window boundaries/carry-over, cooldown boundaries, suppressed events not extending cooldown, stale thresholds, bounded storage and parser filtering. [Test output](../../Tools-And-Methods/UFW-Scan-Watcher/offline-test-results.txt) is published. This verifies replacement logic for supplied inputs, not historical watcher behaviour or live coverage.

Owner-supplied installer output records the tests passing again, the user-service enablement symlink, active status and service start. A later read-only journal check showed the Python startup message. The owner confirmed a separately sent test notification appeared; this checks desktop presentation, not detector-to-notification integration.

**Open limits:** live network/log-to-alert delivery and watcher persistence across login/reboot have not been tested. Current block logs are rate-limited to three/minute, burst ten; thirty packets cannot be assumed to yield thirty counted records. Slow probes, accepted traffic and router-blocked traffic remain outside reliable coverage. The watcher is a user-session alerting control, not an automatic blocking control. Source eviction, delivery delays, restart and notification-failure semantics are documented with its source.

### Follow-up scope and closure

| Item | Current evidence | Remaining gap |
| --- | --- | --- |
| V1 | One reboot retains the inspected restored ping/IPv6 settings, DROP rule and active UFW | All other historical controls, future updates and complete configuration/version manifest remain unverified |
| V2 | DROP delta, scoped ACCEPT/timeouts, positive replies and cleanup | Full independent-control matrix and packet captures remain absent |
| V3 | New source/tests published; boundary logic passes offline; service installed/active; standalone notification visible | Live ingestion-to-alert and session/reboot persistence remain untested |

## Safe verification procedures

The procedures below are guidance for repeat/further verification, not a transcript of tests already run. Keep completed evidence and remaining gaps distinct.

### V1: repeatable reboot verification

Use a local console and a planned maintenance period on the original workstation; save work and confirm recovery access first. Do not reboot through a remote-only session. Save captures privately, review/redact before publishing, and preserve command failures as evidence. Capture versions, configuration files and hashes, including all sysctl sources and UFW's `IPT_SYSCTL` target. Do not run `sysctl --system`, restart UFW, or otherwise reapply policy before the first post-boot capture.

Run this block before reboot and again immediately after boot, saving terminal output in separate `V1-before.txt` and `V1-after.txt` files:

```sh
date -u --iso-8601=seconds
cat /proc/sys/kernel/random/boot_id
uname -r
ufw version
sysctl net.ipv4.icmp_echo_ignore_all
sudo ufw status verbose
systemctl is-enabled ufw.service
systemctl is-active ufw.service
sudo ufw show raw
sudo journalctl -b -u ufw.service --no-pager
sudo journalctl -b -u systemd-sysctl.service --no-pager
sudo rg -n 'icmp_echo_ignore_all|IPT_SYSCTL' /etc/sysctl.conf /etc/sysctl.d /run/sysctl.d /usr/local/lib/sysctl.d /usr/lib/sysctl.d /etc/ufw/sysctl.conf /etc/default/ufw
```

After the before capture, reboot from the local console with `sudo systemctl reboot`. Confirm boot IDs differ. Compare the live value, active service and effective DROP rule; boot enablement alone is insufficient. After the untouched after capture, run `sudo ufw reload`, capture its exit status/output, then repeat `sysctl net.ipv4.icmp_echo_ignore_all` and `sudo ufw show raw` into `V1-after-reload.txt`. Report reboot and reload outcomes separately. This scoped check does not reverify all 35 entries; extending that claim requires the exact key/value inventory and individual post-boot read-backs, including current interfaces.

### V2: independent IPv4 ping controls

Perform policy changes only in a disposable VM clone with the same UFW configuration, a local console and snapshot. Attach it and a test peer solely to a private virtual switch with no uplink, NAT, forwarding or other guests. Do not run these changes on the daily workstation. Record clone/version differences. The addresses below are examples assigned exclusively to that isolated link: peer `192.0.2.2`, target `192.0.2.1`; replace `LAB_IF` with the target's verified private interface name.

Before changing anything, save `sudo ufw show raw`, `sudo iptables-save -c`, `sudo nft list ruleset` and `sysctl net.ipv4.icmp_echo_ignore_all`. Inspect actual rule order/backend: proceed with the commands below only if UFW uses the inspected iptables INPUT path and there are no other hooks dropping the test flow. If it uses another path, stop and draft a backend-specific scoped rule from that ruleset. Do not flush rules or disable UFW.

On the target, keep `sudo tcpdump -ni LAB_IF -w V2.pcap 'icmp and host 192.0.2.2'` running in another console. For each row capture UTC time, live sysctl, full rule counters before/after, and on the peer run `ping -4 -n -c 3 -i 1 -W 1 192.0.2.1`, preserving output and exit status. Capture on the peer too if reply delivery is uncertain.

| Order | Scoped INPUT exception | Live kernel value | Expected result, not yet observed |
| --- | --- | --- | --- |
| 1: positive control | ACCEPT below installed | `0` | Requests arrive and replies return; otherwise stop, since the path is not validated. |
| 2: kernel alone | Same ACCEPT remains | `1` | ACCEPT counter increases, requests arrive, no replies leave target. |
| 3: positive recheck | Same ACCEPT remains | `0` | Replies return again. |
| 4: firewall alone | Exception removed; original UFW DROP applies | `0` | Requests arrive, original DROP counter increases, no replies. |
| 5: combined policy | Original UFW rules | `1` | No replies; this row alone does not attribute effectiveness. |

Use these exact mutations in that order; verify each succeeds before moving on. The temporary rule bypasses the firewall for only this peer's Echo Requests on the private interface:

```sh
# Row 1
sudo iptables -I INPUT 1 -i LAB_IF -s 192.0.2.2 -d 192.0.2.1 -p icmp --icmp-type echo-request -m comment --comment portfolio-V2 -j ACCEPT
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=0
# Capture row 1, then row 2
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=1
# Capture row 2, then row 3
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=0
# Capture row 3, then remove the exact exception for row 4
sudo iptables -D INPUT -i LAB_IF -s 192.0.2.2 -d 192.0.2.1 -p icmp --icmp-type echo-request -m comment --comment portfolio-V2 -j ACCEPT
# Capture row 4, then row 5
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=1
```

Use `sudo iptables-save -c` for counter captures; do not reset counters. Save live values after every mutation and do not reload UFW mid-matrix. On error, stop traffic and revert the VM snapshot. At completion stop captures, confirm the exception is absent, save final rules/value, disconnect the private switch and revert/delete the clone. These tests establish behaviour on the recorded clone, not untested workstation behaviour, IPv6 policy or useful ICMP error handling. The kernel setting's meaning is documented in the [Linux kernel IP sysctl reference](https://kernel.org/doc/html/latest/networking/ip-sysctl.html); rule insertion/deletion is described in the [iptables manual](https://www.man7.org/linux/man-pages/man8/iptables.8.html).

### V3: watcher threshold, window and cooldown

The historical watcher source was not recovered. The replacement source, service and deterministic tests are now published in [Tools-And-Methods/UFW-Scan-Watcher](../../Tools-And-Methods/UFW-Scan-Watcher/README.md). The following matrix describes further checks; offline replacement tests already completed are identified above. Do not invent a command, assume packet count equals parsed attempts, or inject synthetic events into the production journal/desktop notifier. First obtain a redacted copy of the deployed script, config and service definition; record hashes/versions and inspect the parser, qualifying log prefix, deduplication, per-source key, clock used, pruning comparison, notification and cooldown reset logic. Establish whether the 60-second window is rolling or fixed, whether exactly 60 seconds is retained, and whether cooldown eligibility is `>=600` or `>600` seconds from the last alert. These boundary semantics are currently unknown.

Create an offline harness around that exact parser/decision code with an injected clock and a recording notifier. Use raw fixtures in the actual deployed log format; never substitute a reimplementation of the detector. Reset state between cases unless a case explicitly tests retained state. Every fixture records event time, delivery time, source, protocol and destination port. Use source A `192.0.2.2`, source B `192.0.2.3` and one blocked TCP port, so the eight-distinct-pair branch cannot explain the 30-attempt result. Times below are relative seconds, not real waits.

| Case | Exact input schedule | Assertion / evidence required |
| --- | --- | --- |
| Attempt threshold | A: 29 qualifying records at times `0..28`; 30th at `29`; 31st at `30` | No alert through 29; one alert on 30; no additional alert on 31 during cooldown. Record parsed count and notification calls. |
| Source isolation | A: 29 at `0..28`; B: one at `29`; A: one at `30` | B must not complete A's count; A's next record reaches 30. |
| Distinct branch regression | A: seven distinct blocked TCP ports at `0..6`; eighth at `7` | Alert on eighth; label separately from attempt-threshold proof. |
| Rolling-window edge | Fresh state for each run: A: 29 records at `0`; one at `59.999`, `60.000`, or `60.001` respectively | Under a rolling window: alert before 60, no alert after 60. At exactly 60 document the inspected comparator and result, rather than assuming inclusivity. If the implementation uses a fixed window, record its epoch and test both sides of its actual boundary instead. |
| Window carry-over | A: 29 at `0`; one at `60.001`; then 28 at `60.002`; final one at `60.003` | For rolling expiry, no alert at the first two later batches (1 then 29 current attempts), alert on the final record (30). Old attempts must not leak into the new window. |
| Cooldown edge | Fresh run for each offset: trigger A with 30 records at `0`; deliver another qualifying 30-record burst at `599.999`, `600.000`, or `600.001` | Suppress before 600; permit after 600 if a fresh threshold is satisfied. Exact equality follows the inspected comparator. Record whether suppressed events accumulate/reset counts and whether they extend cooldown. |
| Cooldown per source | Trigger A at `0`; trigger B with 30 records at `1` | B can alert independently of A's cooldown. |
| No delayed alert without threshold | Trigger A at `0`; no input until a single A record at `600.001` | Expired records alone must not create a fresh threshold; record timer-driven behaviour if present. |

If timestamp precision is whole seconds, use `59/60/61` and `599/600/601` and disclose the reduced resolution. If time is read at delivery, advance the injected delivery clock; changing text timestamps alone will not test expiry. Inspect and separately report restart/log rotation, late timestamps and clock changes; they are outside closure of this narrow follow-up unless encountered.

After offline cases pass, use the same isolated clone/peer arrangement for one integration check: send 29 then one TCP SYN to a single confirmed blocked port within 60 seconds, using an installed packet tool with retries disabled; capture on both ends. Record emitted packets, firewall log records, parsed attempts and notification calls separately. If logging limits yield fewer than 30 qualifying records, mark the integration result inconclusive for the threshold, retain the logging-loss evidence and do not increase traffic on the workstation. For a peer with `hping3` already installed, and only after confirming TCP port `65000` is blocked on the isolated target, use:

```sh
sudo hping3 -S -p 65000 -c 29 -i u500000 192.0.2.1
# Capture watcher state/count and absence of notification immediately, then:
sudo hping3 -S -p 65000 -c 1 192.0.2.1
```

Do not wait more than the remaining 60-second window between commands. If the tool is unavailable, stop and draft the equivalent bounded command for the installed tool; do not substitute a full port scan. Save the exact command, timestamps and log cursor range. Offline replay proves logic for supplied inputs; it does not prove live logging coverage or desktop notification delivery.

### Evidence handling and documentation closure

Store command transcripts with exit statuses, UTC times, boot IDs, version/config hashes, scoped packet captures, counter deltas, raw fixtures, harness revision and expected/actual notification traces. Keep originals private; publish reviewed redacted derivatives with an evidence manifest identifying omissions. For each V1–V3 record `not run`, `pass`, `fail` or `inconclusive`, environment and evidence link. Update only the matching register row and case-study result after reviewing that evidence. Preserve historical results and unclosed limits; do not mark all three complete from one successful ping or alert.

[Control register](../../Risk-And-Controls/Host-Hardening-Control-Register.md) · [Investigation methods](../../Tools-And-Methods/README.md)
