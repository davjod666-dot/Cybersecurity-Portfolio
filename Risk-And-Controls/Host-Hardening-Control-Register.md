# Host-Hardening Control Register

**Assessment date:** 1 October 2026

**Scope:** Personal Omarchy workstation; live configuration and isolated network checks.

**Owner:** David Seabrook

**Implementation:** AI-assisted review, changes, and test execution.

| Objective | Implemented control | Recorded validation | Limit / residual risk |
| --- | --- | --- | --- |
| Limit unsolicited inbound access | Active UFW with default-deny inbound policy | `ufw status verbose` showed active; service enabled at boot | LocalSend and Docker DNS exceptions remain; no external perimeter scan performed |
| Prevent unwanted service activation | SSH, CUPS, and Avahi services and activation units masked | Units inactive and masks present | Changes remove those capabilities; application-level discovery can still exist |
| Keep ping policy consistent | Kernel and UFW sysctl values aligned; inbound Echo Requests dropped | Kernel value `1` after reload; isolated ping received no replies | Ping silence does not make a host invisible |
| Restrict IPv6 use | Kernel disable flags and NetworkManager profile configured | Disable flags `1`; no IPv6 addresses shown | Reboot persistence configured but not validated by reboot |
| Set resolver policy | Cloudflare IPv4 DNS and ignore automatic DNS on the configured network profile | Resolver status showed Cloudflare; test lookup succeeded | DNS over TLS is opportunistic, not enforced; app-specific resolvers may differ |
| Detect bursts of blocked inbound probes | Rate-limited scan logs and desktop watcher | Eight test destination ports triggered an alert | Slow scans, logging limits, allowed ports, and traffic stopped at the router may evade alerts |
| Reduce kernel information exposure | Pointer hiding, restricted kernel logs, restricted unprivileged BPF, and BPF JIT hardening | Applied settings read back after firewall reload | Privileged access and application vulnerabilities remain outside this control |
| Restrict process tracing | Yama `ptrace_scope=1` | Live value read back | Normal child debugging and explicitly permitted relationships remain possible |
| Reject redirect and source-routing changes | IPv4 redirect acceptance/sending and source routing disabled across interfaces | All configured per-interface values checked after UFW reload | This does not authenticate all network traffic |
| Protect shared temporary files | Protected links, regular files, and FIFOs; privileged-process core dumps disabled | Live sysctl values checked | Application permissions and secure coding remain relevant |

## Evidence detail

[UFW/sysctl case study](../Case-Studies/Linux-Hardening/UFW-Sysctl-Conflict.md) contains the conflict, code-path finding, configuration excerpts, and isolated-test result. The table above summarises recorded session checks; a complete raw command-output bundle is not included in this repository.

## Follow-up

- Check settings again after reboot and relevant package updates.
- Review existing firewall exceptions when application needs change.
- Validate detection coverage against slower and distributed probes in an authorised lab.
- Retain redacted output captures alongside future control changes.

No framework compliance status or risk score is assigned by this register.
