# FM PHASE CLOSE NOTE — FM-OTC-002 CONTROLLED EXPOSURE

## Summary

Financial Management has transitioned from a single-outcome baseline (FM-OTC-001) to a governed dual-path model with controlled exposure of FM-OTC-002.

This transition introduces request-governed outcome selection while preserving baseline stability and fail-closed enforcement.

## What is now operational

- Request-controlled outcome selection via `analysis_type`
    - `explain_document` → FM-OTC-001 (default)
    - `cash_flow_multi_period` → FM-OTC-002

- Mutually exclusive governed runtime lock
    - exactly one FM outcome emitted per request

- FM-OTC-002 controlled exposure
    - only available when explicitly requested
    - requires sufficient governed multi-period substrate

- Fail-closed enforcement
    - insufficient multi-period basis results in rejection
    - no degraded or partial FM-OTC-002 emission

- No outward leakage of internal validation or helper fields

## What remains unchanged

- Default behavior remains FM-OTC-001
- Existing FM-OTC-001 contract and outputs unchanged
- Enforcement, consent, and document validation layers unchanged

## Architectural significance

This phase establishes:

- Request-governed outcome selection as the control mechanism
- Safe expansion path for future FM outcomes
- Strict separation between internal validation and outward contract
- Controlled analytical capability exposure without contract drift

## Next phase (not yet started)

- Additional governed FM outcomes (e.g. FM-OTC-003+)
- Possible expansion of analytical coverage under the same request-governed model

No further exposure changes are active beyond FM-OTC-001 and FM-OTC-002 at this stage.

## Status

FM-OTC-002 controlled exposure is operational, governed, and aligned across:
- orchestration layer
- execution layer
- runtime enforcement
- governed documentation

Phase complete.
