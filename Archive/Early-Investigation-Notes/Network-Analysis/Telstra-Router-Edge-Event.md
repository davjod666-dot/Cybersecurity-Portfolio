# Telstra Router Edge Events: DHCP, UPnP, and NAT

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Investigate reported lease activity, changing port mappings, and connection-table events.

## Reported observations

- The earlier notes describe DHCP activity, UPnP mapping changes, and conntrack-related events.
- Discovery traffic was reported during apparently idle periods.
- Actions recorded include disabling UPnP and WAN management, DHCP reservations, DNS changes, and time-source correction.
- The original assessment favoured device or router stability explanations.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The public record does not establish a specific firmware defect, remote intrusion, or causal link between every event. The original hardening actions are recorded as reported actions; a complete baseline and post-change output set is not included.

## Validation requirements

1. Publish redacted router events with accurate timestamps and capture context.
2. Identify which device requested each port mapping and connection.
3. Record firmware version and use vendor evidence before attributing a firmware bug.
4. Compare stability and connection metrics before and after each change.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
