# AWDL Wireless Behaviour and Peer Discovery

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Assess reported discovery traffic and interface activity without assuming either compromise or benignity from a protocol name.

## Reported observations

- The earlier write-up reports awdl0 creation/teardown and discovery traffic.
- mDNS traffic was described after sharing features were disabled.
- The original investigation favoured a background-service explanation.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

The earlier assessment was consistent with a benign explanation, but raw captures, timing, platform context, and baseline comparisons are not public. The available summary cannot independently rule out every malicious discovery scenario or establish which service produced each event.

## Validation requirements

1. Record capture interfaces and whether traffic was visible over the air or only in host logs.
2. Attribute discovery packets to devices and services where possible.
3. Compare enabled/disabled settings under repeatable conditions.
4. Avoid treating a protocol label as sufficient evidence of legitimacy.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
