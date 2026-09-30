# RunningBoard: Assertions, Power Requests, and Task Lifecycle

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Examine reported keepalive, power, and lifecycle assertions involving background services.

## Reported observations

- The earlier notes describe keepalive and idle-sleep-related requests.
- They associate lifecycle events with several Apple service names.
- A device restore was recorded as an action taken.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The summary does not establish process hijacking, privilege escalation, covert data collection, or unauthorised supervision. Request names and service names require context, ownership evidence, and a measured outcome. This case overlaps with the earlier RunningBoard review and focuses specifically on assertion ownership and power requests.

## Validation requirements

1. Include the exact message, source process, target process, result, and timestamp.
2. Distinguish a request from a granted assertion and from its actual effect.
3. Compare activity before and after any restore using the same test conditions.
4. Correlate network endpoints and payload scope before making a data-collection claim.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
