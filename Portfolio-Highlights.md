# Portfolio Highlights

**David Seabrook · AI governance, cyber risk, and security operations**

## A technical finding with a governance outcome

[**Linux hardening and UFW sysctl precedence**](Case-Studies/Linux-Hardening/UFW-Sysctl-Conflict.md)

A host-hardening review found two configuration sources assigning different values to the same ping-suppression setting. Inspection of UFW’s reload code established the override path. Aligning the values removed the conflict; a subsequent firewall reload and an isolated network test checked the live result.

The accompanying [control register](Risk-And-Controls/Host-Hardening-Control-Register.md) records objectives, evidence, limits, and residual risk. The work demonstrates why a configured control and a validated control are different things.

## AI governance and responsible AI

[**AI governance section**](AI-Governance/README.md)

This section connects documented study and current AI evaluation work with an assessment structure: purpose, ownership, data, foreseeable harms, oversight, testing, and change control. The [assessment template](AI-Governance/AI-System-Assessment-Template.md) is a portfolio resource; it is not a completed organisational assessment or a compliance attestation.

## Security operations

[**SOC investigations index**](SOC-Investigations/README.md)

Two original network cases remain visible as learning briefs: the Telstra DHCP/time/WAN review and STUN/multicast correlation. They show investigation questions relevant to SOC triage, with their evidence limits stated. Eleven overlapping or less-supported early notes are preserved in a separate learning archive. The live-tested Linux hardening case leads the technical showcase.

Additional experience described in the supplied CV includes Wazuh and Suricata deployment, a segmented home lab, and an FTP malware-transfer investigation. Supporting project artefacts can be added when ready; the repository does not imply they are already published.

## Professional background

15+ years across emergency services provides a foundation in operational risk, proportionate response, escalation, and legally significant documentation. Current AI evaluation work adds output review, structured annotation, and quality reasoning.

[CV](Documents/CV_David_Seabrook.md) · [Qualifications](Documents/Qualifications.md) · [Investigation methods](Tools-And-Methods/README.md)
