# Port 443 Loopback Activity: Scope and Process Attribution

**Analyst:** David Seabrook

**Original notes:** 2025

**Publication type:** Archived early investigation note; editorial review in October 2026.

## Question

Investigate reported TLS activity involving localhost during apparent system idle.

## Reported observations

- The earlier write-up describes connections involving 127.0.0.1:443.
- Loopback packet captures and host logs were listed as collection sources.
- The original interpretation attributed activity to local services.

These observations are summarised from the earlier write-up. Complete original captures, timestamped logs, and collection metadata are not published here and were not newly authenticated during this editorial review.

## Assessment and limits

A loopback capture can describe local exchanges within its capture window; it cannot by itself exclude separate outbound traffic or establish process legitimacy. The published case lacks socket ownership and a timestamped process-to-flow mapping, so specific service attribution remains unresolved.

## Validation requirements

1. Capture the listening socket and owning process at the event time.
2. Correlate executable identity, service configuration, and connection endpoints.
3. Check external interfaces separately when evaluating outbound traffic.
4. Record certificate/handshake details and observation limits without assuming an encrypted connection is benign.

The steps above identify evidence needed for a stronger assessment; they are not presented as newly completed tests.

## Investigation value

This case focuses on scoping observations, comparing alternative explanations, and identifying the evidence needed for a defensible conclusion. Earlier versions remain available in Git history.

[SOC index](../../../SOC-Investigations/README.md) · [Investigation methods](../../../Tools-And-Methods/README.md)
