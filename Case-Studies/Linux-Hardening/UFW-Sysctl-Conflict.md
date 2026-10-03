# Linux Host Hardening: UFW and sysctl Configuration Conflict

**Analyst:** David Seabrook

**Date:** 1 October 2026

**Environment:** Personal Omarchy Linux workstation

**Scope:** AI-assisted configuration review, implementation, and isolated validation.

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

[Control register](../../Risk-And-Controls/Host-Hardening-Control-Register.md) · [Investigation methods](../../Tools-And-Methods/README.md)
