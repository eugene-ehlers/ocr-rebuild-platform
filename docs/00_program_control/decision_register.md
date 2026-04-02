# Decision Register

## OCR-First Controlled Exposure Decisions

### Decision: FICA OCR-First Controlled Exposure Authority
- decision_id: DR-FICA-OCR-FIRST-001
- status: approved
- scope: fica
- approved_scope_boundary: ocr_first_only
- excluded_scope: bureau|pep|pip|home_affairs|external_compliance_enrichment
- controlled_selector_expectation: selector_must_lock_exactly_one_governed_fica_outcome
- outward_outcome_rule: exactly_one_fica_outcome_may_be_emitted
- fail_closed_rule: insufficient_basis_for_selected_fica_outcome_must_fail_closed
- approved_outcome_codes: FICA-OTC-001|FICA-OTC-002|FICA-OTC-003|FICA-OTC-004|FICA-OTC-005|FICA-OTC-006
- notes: extraction_and_analytical_fica_otcs_must_remain_distinct

### Decision: Credit OCR-First Controlled Exposure Authority
- decision_id: DR-CREDIT-OCR-FIRST-001
- status: approved
- scope: credit_decision
- approved_scope_boundary: ocr_first_only
- excluded_scope: bureau|pep|pip|home_affairs|pricing|offer_generation
- controlled_selector_expectation: selector_must_lock_exactly_one_governed_credit_outcome
- outward_outcome_rule: exactly_one_credit_outcome_may_be_emitted
- fail_closed_rule: insufficient_basis_for_selected_credit_outcome_must_fail_closed
- approved_outcome_codes: Credit-OTC-001|Credit-OTC-002|Credit-OTC-003|Credit-OTC-004|Credit-OTC-005|Credit-OTC-006|Credit-OTC-007|Credit-OTC-008|Credit-OTC-009
- notes: extraction_and_analytical_credit_otcs_must_remain_distinct

---

## End of Document

### Frontend Redesign Alignment to Design Baseline

**Decision**  
The frontend will be incrementally redesigned to align with the approved frontend customer experience design baseline (Steps 1–7).

**Rationale**  
The current frontend is a Developer / Operational Interface (DOI) and not suitable for customer-facing usage.

**Approach**  
- Layered implementation  
- Non-breaking transition  
- Replace DOI behaviour with governed UX model

## DR-frontend-deployment-safety-immutable-releases

### Decision
Frontend deployments for S3 + CloudFront hosted sites must move from mutable live-root overwrite to an immutable release-folder model with controlled promotion.

### Reason
A destructive root deployment pattern caused a production incident affecting company and pilot sites. Root-level overwrite with destructive sync and no versioning or retained releases made rollback difficult and increased blast radius.

### Rule
- live root is logically read-only for deployment
- deployment writes go only to `releases/<release-id>/`
- promotion updates `current/`
- promotion must not use `sync --delete`
- runtime release metadata is required
- CloudFront serving `current/` is the governed target state

### Status
Approved
