# Host-Hardening Control Register

**Assessment date:** 1 October 2026

**Scope:** Personal Omarchy workstation; recorded configuration read-backs and isolated network checks from the assessment session.

**Owner:** David Seabrook

**Implementation:** David Seabrook defined the workstation requirements and requested the hardening changes. Codex assisted with configuration and code inspection, implementation, and test execution.

| Objective | Implemented control | Recorded validation | Limit / residual risk |
| --- | --- | --- | --- |
| Limit unsolicited inbound access | Active UFW with default-deny inbound policy | `ufw status verbose` reported active; the service was recorded as enabled for boot. Boot-time activation was not tested by rebooting. | LocalSend and Docker DNS exceptions remain; no external perimeter scan performed |
| Prevent unwanted service activation | SSH, CUPS, and Avahi services and activation units masked | Units inactive and masks present | Changes remove those capabilities; application-level discovery can still exist |
| Keep ping policy consistent | Kernel and UFW sysctl values aligned; firewall rule configured to drop inbound Echo Requests | Conflicting configuration values and the installed UFW reload path were inspected; after alignment and reload, the kernel value was `1`. An isolated ping test received no replies. | The pre-fix reset was not deliberately reproduced. The no-reply result does not establish the firewall and kernel controls independently; ping silence does not make a host invisible. |
| Restrict IPv6 use | Kernel disable flags and NetworkManager profile configured | Disable flags `1`; no IPv6 addresses shown | Reboot persistence configured but not validated by reboot |
| Set resolver policy | Cloudflare IPv4 DNS and ignore automatic DNS on the configured network profile | Resolver status showed Cloudflare; test lookup succeeded | DNS over TLS is opportunistic, not enforced; app-specific resolvers may differ |
| Detect bursts of blocked inbound probes | Rate-limited scan logs and desktop watcher | Probes to eight blocked TCP destination ports from the isolated test source generated an alert. | Slow scans, logging limits, allowed ports, and traffic stopped at the router may evade alerts. Separate tests of the 30-attempt threshold, 60-second window boundaries, and ten-minute cooldown are not documented. |
| Reduce kernel information exposure | Pointer hiding, restricted kernel logs, restricted unprivileged BPF, and BPF JIT hardening | Applied settings read back after firewall reload | Privileged access and application vulnerabilities remain outside this control |
| Restrict process tracing | Yama `ptrace_scope=1` | Live value read back | Normal child debugging and explicitly permitted relationships remain possible |
| Reject redirect and source-routing changes | IPv4 redirect acceptance/sending and source routing disabled across interfaces | All configured per-interface values checked after UFW reload | This does not authenticate all network traffic |
| Protect shared temporary files | Protected links, regular files, and FIFOs; privileged-process core dumps disabled | Live sysctl values checked | Application permissions and secure coding remain relevant |

## Evidence detail

The [UFW/sysctl case study](../Case-Studies/Linux-Hardening/UFW-Sysctl-Conflict.md) describes the inspected configuration conflict and reload code path, the changes, and recorded post-change results. This register summarises recorded session checks; a complete raw command-output bundle is not included in this repository. Configuration and live-value checks establish the settings inspected, not the effectiveness of every control against network traffic or exploitation. The case study’s read-only commands are verification guidance, not a preserved session transcript, and do not verify every row of this register. Reboot persistence was not tested; this limitation applies across the register.

## Follow-up

- Check settings again after reboot and relevant package updates.
- Review existing firewall exceptions when application needs change.
- Validate detection coverage against slower and distributed probes in an authorised lab.
- Retain redacted output captures alongside future control changes.

No framework compliance status or risk score is assigned by this register.
