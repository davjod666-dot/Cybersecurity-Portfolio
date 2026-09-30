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

Inspection of the installed `/usr/lib/ufw/ufw-init-functions` showed that `ufw_reload()` invokes `ufw_start()`. Startup loads the file identified by `IPT_SYSCTL`, which pointed to `/etc/ufw/sysctl.conf` on this workstation. This establishes an override path.

The conflicting files and installed code were inspected. A reset was not deliberately reproduced before fixing the configuration, so this case does not claim a captured pre-fix failure on an untouched installation.

## Change

- Aligned both configuration sources to `icmp_echo_ignore_all=1`.
- Retained a firewall DROP rule for inbound ICMP Echo Requests.
- Preserved useful ICMP error handling and replies to outbound connections.
- Backed up configuration and recorded live values before broader sysctl hardening.

The firewall silently drops incoming requests. The kernel setting provides a separate control if requests reach the kernel echo handler.

## Validation

| Check | Result |
| --- | --- |
| Kernel value after UFW reload | `net.ipv4.icmp_echo_ignore_all = 1` |
| Ping from an isolated temporary network | No replies |
| Eight blocked TCP destination ports from the test source | Scan detector generated an alert |
| DNS query after hardening | Successfully resolved |
| Firewall and desktop monitor | Active |
| Sysctl hardening settings after UFW reload | All 35 configured entries verified, including per-interface values |

The temporary network was removed after testing. Scan alerts use a 60-second window and trigger at eight distinct blocked protocol/port pairs or 30 attempts from one source, with a ten-minute per-source cooldown.

## Limits

- This is a configuration conflict, not a finding that normal ping replies are a vulnerability.
- A clean-install reproduction has not established an Omarchy-specific bug.
- Ping suppression does not conceal allowed services.
- The scan watcher cannot see traffic blocked by the router; slow scans and logging-rate limits reduce coverage.
- Boot persistence is configured but was not tested by rebooting.
- The checks are documented session results; full raw output is not published here.

## Control-assurance lesson

Configuration files are evidence of intended policy. Read-back checks and controlled tests provide evidence of current behaviour. Check all services that can apply the same kernel setting, then validate after they reload.

## Read-only checks for the current configuration

On this workstation, the following checks inspect the live setting, its configuration sources, and the installed UFW reload code:

```sh
sysctl net.ipv4.icmp_echo_ignore_all
rg -n 'icmp_echo_ignore_all' /etc/sysctl.d/ /etc/ufw/sysctl.conf
rg -n 'ufw_reload|ufw_start|IPT_SYSCTL|sysctl' /usr/lib/ufw/ufw-init-functions /etc/default/ufw
```

Expected policy: both configuration sources assign `1`, and the live value is `1`. These commands are a verification guide, not a preserved transcript of the original test. A read-back alone does not reproduce the network test or prove reboot persistence.

[Control register](../../Risk-And-Controls/Host-Hardening-Control-Register.md) · [Investigation methods](../../Tools-And-Methods/README.md)
