# AWDL Discovery Under Unexpected Device Conditions

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Investigate reported peer-discovery activity when sharing features or Wi-Fi appeared disabled.

## Reported observations

- The earlier notes describe awdl0 activation and discovery-related events.
- Multicast activity and channel-related messages were associated with idle or locked states.
- The meaning of the visible Wi-Fi control was central to the original question.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The public notes do not establish a wireless-control bypass, malicious peer discovery, or an actor maintaining presence. The exact control used, platform version, capture interface, and observed packets are needed to evaluate expected versus unexpected activity.

## Validation requirements

1. Record the precise control path used to change Wi-Fi and sharing settings.
2. Collect over-the-air or interface-specific evidence with timestamps.
3. Distinguish interface lifecycle messages from transmitted frames and established sessions.
4. Compare against documented platform behaviour and a controlled baseline.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
