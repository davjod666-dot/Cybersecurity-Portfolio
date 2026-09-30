# Skywalk and FlowSwitch: Cross-Subsystem Correlation

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Correlate networking messages with RunningBoard, discovery, and reachability events.

## Reported observations

- The earlier notes describe nexus creation, flow attachment, and NetworkExtension resets.
- They correlate those messages with RunningBoard, STUN, and AWDL observations.
- The original interpretation proposed a non-visible routing layer.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The proposed routing-layer explanation is a hypothesis. No timestamped multi-source timeline, route changes, interface ownership, or packet destinations are published to demonstrate it. Timing correlation alone does not establish covert coordination, persistence, or external control.

## Validation requirements

1. Create a single timeline with source references and clock-offset handling.
2. Link events through shared PIDs, flow identifiers, interface names, or packet endpoints.
3. Document which competing explanations each test supports or weakens.
4. Capture route/interface changes and traffic outcomes before attributing a hidden tunnel.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
