# Skywalk and NetworkExtension: Interface and Flow Review

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Investigate networking subsystem messages when no user-installed VPN was reported.

## Reported observations

- Earlier notes mention nexus/flow attachment and NetworkExtension activation events.
- Socket and DNS-related events were described alongside disabled-network or locked-device states.
- Some activity was reported after reset or permission changes.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The presence of a framework or flow message does not demonstrate a hidden VPN, external control, or successful packet transmission. The public summary lacks route, interface, endpoint, and process evidence needed to establish that interpretation.

## Validation requirements

1. Collect interface and routing state alongside the relevant log window.
2. Identify the process and configuration responsible for each flow.
3. Verify successful traffic on the capture interface rather than equating a socket event with transmission.
4. Compare before/after configuration states and a known-good baseline.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
