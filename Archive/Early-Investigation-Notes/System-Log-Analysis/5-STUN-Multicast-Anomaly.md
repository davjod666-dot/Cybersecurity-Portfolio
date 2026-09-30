# STUN and Multicast Activity During Idle Device States

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Investigate discovery and reachability-related traffic reported while devices were idle, locked, or believed offline.

## Reported observations

- The earlier notes report activity on UDP 3478 and multicast/discovery-related events.
- Traffic bursts were described near RunningBoard wake events.
- Some events were associated with airplane-mode or disabled-network observations.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

Port numbers and coincident events alone do not establish the protocol, application owner, remote reachability, or malicious purpose. The reported state discrepancy remains an investigation question without a timestamped capture and exact radio-state record.

## Validation requirements

1. Decode representative packets to confirm protocol identification.
2. Record the capture point, interface, endpoints, direction, and device state.
3. Check whether events are attempts, successful exchanges, or historical messages.
4. Test alternative application/system explanations and align clock offsets before correlating sources.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
