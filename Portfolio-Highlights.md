# Portfolio Highlights

**David Seabrook · Junior cyber GRC and security assurance**

## Completed workstation exercise

[Linux hardening: UFW/sysctl configuration conflict](Case-Studies/Linux-Hardening/UFW-Sysctl-Conflict.md)

Two configuration files assigned different values to the ping-suppression setting. An AI-assisted review inspected UFW’s reload path, aligned the settings, and checked the live value after reload. An isolated network test received no ping replies and triggered the configured scan alert.

The case includes configuration excerpts, recorded results, and limitations. Full raw test output is not published. The pre-fix reset was not deliberately reproduced. After a reinstall, the 6–7 October follow-up restored ping and IPv6 policy and verified the inspected settings across one reboot. LAN ping tests supported firewall dropping and kernel suppression, with manually reported Windows results and no packet capture. A replacement scan watcher was installed and its ten offline tests passed; live scan-to-alert delivery and watcher reboot persistence remain untested.

[Host-hardening control register](Risk-And-Controls/Host-Hardening-Control-Register.md)

This companion document records each control’s objective, validation, remaining risk, and follow-up. It is a personal-workstation example, without an enterprise compliance claim.

## AI governance learning

[AI governance section](AI-Governance/README.md)

Coursework and an unfilled assessment template cover system ownership, data flows, foreseeable harms, control testing, and human oversight. A completed applied assessment is not yet published.

## Defensive lab practice

[Defensive practice](SOC-Investigations/README.md)

My home-lab experience includes VLAN segmentation, Wazuh, Suricata, and packet analysis. Architecture, alert-investigation, and packet-timeline artefacts are still to publish.

## Professional background

15+ years in emergency services contributes experience in operational risk, triage, escalation, and clinical and statutory documentation. My current AI contracting work involves reviewing generated outputs and applying annotation criteria.

[CV](Documents/CV_David_Seabrook.md) · [Qualifications](Documents/Qualifications.md)
