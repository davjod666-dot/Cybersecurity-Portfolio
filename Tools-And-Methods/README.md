# Tools & Investigation Methods

This is the documentation standard for future work and updates to retrospective cases. It does not imply every historical investigation already meets every requirement.

## Investigation structure

1. **Question and scope:** system, symptom, collection window, and authorisation.
2. **Collection:** source, tool, version, timezone, collection method, and original-artifact retention.
3. **Observations:** redacted excerpts or packet fields with timestamps and source references.
4. **Timeline:** account for clock offsets before correlating sources.
5. **Hypotheses:** expected behaviour, configuration issues, and security explanations where evidence warrants them.
6. **Validation:** controlled tests or baseline comparisons, with expected and observed results.
7. **Assessment:** supported findings, uncertainty, and remaining questions.
8. **Control decision:** actions, backups, rollback, verification, and residual risk.

## Evidence rules

- A framework or process name alone does not establish malicious behaviour.
- Timing correlation does not, by itself, establish causation.
- A capture covers only its collection point, interfaces, and time window.
- Process attribution should include the method used and capture-time ownership evidence.
- Distinguish raw excerpts, paraphrased examples, and analyst interpretation.
- Redact personal identifiers, credentials, and unrelated third-party information before publication.
- Distinguish course completion, lab practice, and production experience.
- Identify AI-assisted analysis or implementation where it materially contributes to the work.

## Tools and sources

| Tool / source | Use |
| --- | --- |
| Wireshark / tcpdump | Packet inspection and capture context |
| Wazuh / Suricata | Home-lab endpoint visibility, log aggregation, and intrusion detection |
| Host logs / sysdiagnose | Process and subsystem investigation |
| Router logs | DHCP, WAN, NAT, and discovery-event context |
| UFW / sysctl / systemd | Firewall, kernel settings, and service-state validation |
| Git / GitHub | Versioned documents and reviewable changes |

See [SOC investigations](../SOC-Investigations/README.md) for the distinction between published case summaries and CV-reported lab projects.

## Published implementation

[Replacement UFW scan watcher](UFW-Scan-Watcher/README.md): source, user-service installer, deterministic threshold/timing tests and documented coverage limits.
