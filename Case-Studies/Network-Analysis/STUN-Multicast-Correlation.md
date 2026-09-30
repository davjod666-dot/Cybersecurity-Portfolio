# STUN and Multicast: Cross-Device Timeline Review

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Selected retrospective learning brief; editorial review in October 2026.

## Question

Correlate reported network-discovery bursts with router and endpoint activity.

## Reported observations

- The original summary lists STUN, mDNS, SSDP, neighbour-discovery, and NAT events.
- Router, macOS, iOS, and smart-device sources were described.
- The investigation favoured scheduled discovery and device activity over an intrusion explanation.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The notes support a benign hypothesis but do not publish a correlated timeline, endpoint attribution, or capture coverage sufficient to prove the proposed cause. The absence of an indicator in an unspecified capture is not a general finding that no intrusion occurred.

## Validation requirements

1. Publish representative protocol fields, endpoints, and timestamps.
2. Align source clocks and identify the capture point for each event.
3. Test whether scheduled device activity explains the observed burst.
4. Document indicators checked, visibility limits, and unresolved alternatives.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../SOC-Investigations/README.md) · [Investigation methods](../../Tools-And-Methods/README.md)
