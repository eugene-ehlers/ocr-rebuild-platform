# Governed Document Map

## Controlled Exposure Authority — FICA OCR-First

The following governed files jointly define the approved documentation baseline for current FICA controlled exposure under OCR-first scope:

- `docs/00_program_control/decision_register.md`
- `docs/20_service_design/fica_input_to_outcome_rule_table_v1.md`
- `docs/20_service_design/fica_outcome_to_capability_rule_table_v1.md`
- `docs/20_service_design/fica_payloads_v1.md`
- `docs/03_data_model/pipeline_s3_payload_contract.md`

Interpretation constraints:

- selector must lock exactly one governed FICA outcome
- runtime selection must remain mutually exclusive
- exactly one outward governed FICA outcome may be emitted
- insufficient basis for the selected governed FICA path must fail closed
- current app scope is OCR-first only
- bureau, PEP, PIP, and Home Affairs scope are excluded from this app

Approved FICA outcomes:
- FICA-OTC-001 Identity document OCR extraction
- FICA-OTC-002 Identity field consistency check
- FICA-OTC-003 Proof-of-address OCR extraction
- FICA-OTC-004 Proof-of-address validity / recency
- FICA-OTC-005 Business registration OCR extraction
- FICA-OTC-006 Business ownership / authority consistency

## Controlled Exposure Authority — Credit OCR-First

The following governed files jointly define the approved documentation baseline for current Credit controlled exposure under OCR-first scope:

- `docs/00_program_control/decision_register.md`
- `docs/20_service_design/credit_input_to_outcome_rule_table_v1.md`
- `docs/20_service_design/credit_outcome_to_capability_rule_table_v1.md`
- `docs/20_service_design/credit_decision_payloads_v1.md`
- `docs/03_data_model/pipeline_s3_payload_contract.md`

Interpretation constraints:

- selector must lock exactly one governed Credit outcome
- runtime selection must remain mutually exclusive
- exactly one outward governed Credit outcome may be emitted
- insufficient basis for the selected governed Credit path must fail closed
- current app scope is OCR-first only
- bureau, PEP, PIP, Home Affairs, pricing, and offer-generation scope are excluded from this app

Approved Credit outcomes:
- Credit-OTC-001 Payslip OCR extraction
- Credit-OTC-002 Payslip income validity check
- Credit-OTC-003 Bank statement OCR extraction
- Credit-OTC-004 Bank statement income signal assessment
- Credit-OTC-005 Bank statement expense signal assessment
- Credit-OTC-006 Payslip-to-bank income consistency
- Credit-OTC-007 OCR-based affordability snapshot
- Credit-OTC-008 Credit document pack completeness
- Credit-OTC-009 OCR-based credit recommendation

---

## End of Document
