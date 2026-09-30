# Device-State Correlation: UI Settings and Backend Events

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Bring the reported device-state observations into a single review matrix without treating correlation as proof of compromise.

## Reported observations

- The earlier notes compare Wi-Fi, airplane-mode, VPN, privacy, and idle-state indications with subsystem events.
- RunningBoard, AWDL, STUN, Skywalk, and NetworkExtension appear across the summaries.
- A restore and fresh-device comparison were recorded or proposed as follow-up.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

This is a correlation exercise, not a demonstrated root cause. A visible setting may describe a narrower scope than all subsystem activity; that scope must be established for each row. The public record does not prove UI masking, unauthorised supervision, telemetry exfiltration, or compromise.

## Validation requirements

1. Publish a matrix containing exact setting, timestamp, event excerpt, and source.
2. State what the setting is expected to control before calling the event inconsistent.
3. Record baseline comparisons, test results, and unanswered questions.
4. Only promote a hypothesis to a finding when the corresponding validation evidence is available.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
