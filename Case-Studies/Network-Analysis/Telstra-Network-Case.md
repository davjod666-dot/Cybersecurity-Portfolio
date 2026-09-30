# Telstra Router Review: DHCP, Management Traffic, and WAN Events

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Selected retrospective learning brief; editorial review in October 2026.

## Question

Investigate reported lease renewals, management traffic, clock drift, and WAN instability.

## Reported observations

- The earlier notes describe DHCP renewals and TR-069-related traffic.
- Time drift was associated with HTTPS/certificate errors.
- WAN events were compared with reported outages and maintenance windows.
- The notes report that time resynchronisation resolved observed errors.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The investigation favoured service-management and stability explanations. The published summary does not include management endpoint validation, lease values, outage references, or before/after timestamps sufficient to independently establish all causal claims. Malicious control was not established in the published notes.

## Validation requirements

1. Record the router model, firmware, event timestamps, and clock offset.
2. Verify management endpoints against provider information.
3. Compare DHCP values and lease timing with the actual configuration.
4. Include outage references and before/after evidence for time-related error resolution.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../SOC-Investigations/README.md) · [Investigation methods](../../Tools-And-Methods/README.md)
