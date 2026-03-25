from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import os
import uuid

from services.decision_engine.engine import execute_service_family
from services.decision_engine.request_store import (
    get_customer_consent_records,
    get_request,
    revoke_customer_consent,
    save_consent_record,
    save_request,
    update_request,
)


SUPPORTED_SERVICE_FAMILIES = {
    "financial_management": {
        "service_code_aliases": {
            "financial_management",
            "transaction_parsing",
            "category_classification",
            "cash_flow_classification",
            "debt_detection",
            "behavioural_analysis",
            "benchmarking",
            "reporting_explanation",
            "translation",
        }
    },
    "fica": {
        "service_code_aliases": {
            "fica",
            "fica_compliance",
            "transaction_compliance_classification",
            "document_validation",
            "identity_owner_verification",
        }
    },
    "credit_decision": {
        "service_code_aliases": {
            "credit_decision",
            "affordability",
            "prevet",
            "bureau_assessment",
            "offer_generation",
        }
    },
}


EXPECTED_DOCUMENT_TYPES = {
    "financial_management": {"bank_statement"},
    "fica": {"identity_document", "proof_of_address"},
    "credit_decision": {"bank_statement", "identity_document"},
}

DEFAULT_VALIDITY_SECONDS = {
    "processing": 60 * 60 * 24 * 30,
    "disclosure": 60 * 60 * 24 * 7,
}

ENFORCEMENT_MODE = "hard"


FM_GOVERNED_RUNTIME_LOCKS = {
    "explain_document": {
        "service_code": "financial_management",
        "service_family": "financial_management",
        "governed_outcome_code": "FM-OTC-001",
        "outcome_result_key": "fm_otc_001",
        "outcome_intent": "explain_document",
        "analysis_type": "explain_document",
    },
    "cash_flow_multi_period": {
        "service_code": "financial_management",
        "service_family": "financial_management",
        "governed_outcome_code": "FM-OTC-002",
        "outcome_result_key": "fm_otc_002",
        "outcome_intent": "analyse_cash_flow",
        "analysis_type": "cash_flow_multi_period",
    },
    "spend_analysis_multi_period": {
        "service_code": "financial_management",
        "service_family": "financial_management",
        "governed_outcome_code": "FM-OTC-003",
        "outcome_result_key": "fm_otc_003",
        "outcome_intent": "analyse_spending_patterns",
        "analysis_type": "spend_analysis_multi_period",
    },
}


@dataclass
class OrchestrationContext:
    request_id: str
    customer_id: str
    service_code: str
    service_family: str
    document_ids: List[str]
    disclose_to_third_party: bool
    analysis_type: Optional[str]
    governed_outcome_code: Optional[str]
    governed_outcome_intent: Optional[str]
    created_at: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    return datetime.fromisoformat(ts)


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def _new_consent_id() -> str:
    return f"consent_{uuid.uuid4().hex[:10]}"


def _new_plan_id(request_id: str) -> str:
    return f"plan_{request_id}"


def _resolve_service_family(service_code: str) -> str:
    normalized = (service_code or "").strip().lower()
    for family, cfg in SUPPORTED_SERVICE_FAMILIES.items():
        if normalized in cfg["service_code_aliases"]:
            return family
    raise ValueError(f"Unsupported service_code: {service_code}")


def _normalize_analysis_type(raw_value: Any) -> str:
    normalized = str(raw_value or "").strip().lower()
    return normalized or "explain_document"


def _resolve_financial_management_runtime_lock(analysis_type: str) -> Dict[str, Any]:
    runtime_lock = FM_GOVERNED_RUNTIME_LOCKS.get(analysis_type)
    if runtime_lock is None:
        raise ValueError(
            "analysis_type must be one of: explain_document, cash_flow_multi_period, spend_analysis_multi_period"
        )
    return dict(runtime_lock)


def _build_context(payload: Dict[str, Any]) -> OrchestrationContext:
    customer_id = str(payload.get("customerId", "")).strip()
    service_code = str(payload.get("serviceCode", "")).strip()
    document_ids = payload.get("documentIds", [])
    disclose = bool(payload.get("discloseToThirdParty", False))

    if not customer_id:
        raise ValueError("customerId is required")
    if not service_code:
        raise ValueError("serviceCode is required")
    if not isinstance(document_ids, list) or not document_ids:
        raise ValueError("documentIds must be a non-empty list")

    service_family = _resolve_service_family(service_code)

    selected_analysis_type: Optional[str] = None
    selected_governed_outcome_code: Optional[str] = None
    selected_governed_outcome_intent: Optional[str] = None

    if service_family == "financial_management":
        runtime_lock = _resolve_financial_management_runtime_lock(
            _normalize_analysis_type(payload.get("analysis_type"))
        )
        selected_analysis_type = runtime_lock["analysis_type"]
        selected_governed_outcome_code = runtime_lock["governed_outcome_code"]
        selected_governed_outcome_intent = runtime_lock["outcome_intent"]

    if (
        service_code == "financial_management"
        and service_family != FM_GOVERNED_RUNTIME_LOCKS["explain_document"]["service_family"]
    ):
        raise ValueError("financial_management runtime lock service_family mismatch")

    return OrchestrationContext(
        request_id=_new_request_id(),
        customer_id=customer_id,
        service_code=service_code,
        service_family=service_family,
        document_ids=[str(x) for x in document_ids],
        disclose_to_third_party=disclose,
        analysis_type=selected_analysis_type,
        governed_outcome_code=selected_governed_outcome_code,
        governed_outcome_intent=selected_governed_outcome_intent,
        created_at=_utc_now(),
    )


def _base_response(
    *,
    success: bool,
    status: str,
    message: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "success": success,
        "status": status,
        "message": message,
        "data": data,
    }


def _find_reusable_consent(customer_id: str, consent_type: str) -> Optional[Dict[str, Any]]:
    records = get_customer_consent_records(customer_id)
    candidates = [r for r in records if r.get("consent_type") == consent_type]
    if not candidates:
        return None

    candidates.sort(key=lambda r: r.get("captured_at") or "", reverse=True)
    for record in candidates:
        if record.get("status") == "valid" and not record.get("is_expired") and not record.get("revoked", False):
            return record
    return None


def _derive_record_status(record: Dict[str, Any]) -> str:
    if not record.get("required", False):
        return "not_required"
    if record.get("revoked", False):
        return "revoked"
    if not record.get("provided", False):
        return "missing"
    if not record.get("evidence_ref"):
        return "invalid"

    valid_until = _parse_iso(record.get("valid_until"))
    if valid_until and valid_until < datetime.now(timezone.utc):
        return "expired"

    return "valid"


def _build_new_consent_record(consent_type: str, provided: bool, payload: Dict[str, Any], required: bool) -> Dict[str, Any]:
    source = str(payload.get(f"{consent_type}ConsentSource", "ui_checkbox"))
    evidence_ref = str(payload.get(f"{consent_type}ConsentEvidenceRef", "")).strip()
    standing = bool(payload.get(f"{consent_type}StandingConsent", True))
    now = datetime.now(timezone.utc)

    validity_seconds = DEFAULT_VALIDITY_SECONDS[consent_type]
    valid_from = now.isoformat() if provided else None
    valid_until = (now + timedelta(seconds=validity_seconds)).isoformat() if provided and standing else now.isoformat() if provided else None

    record = {
        "consent_id": _new_consent_id(),
        "consent_type": consent_type,
        "required": required,
        "provided": provided,
        "status": "unknown",
        "captured_at": now.isoformat() if provided else None,
        "source": source if provided else None,
        "evidence_ref": evidence_ref if provided else None,
        "standing": standing if provided else False,
        "validity_window_seconds": validity_seconds if provided else None,
        "valid_from": valid_from,
        "valid_until": valid_until,
        "is_expired": False,
        "revoked": False,
        "revoked_at": None,
        "reused": False,
    }

    record["status"] = _derive_record_status(record)
    record["is_expired"] = record["status"] == "expired"
    return record


def _get_or_create_consent_record(customer_id: str, consent_type: str, provided: bool, payload: Dict[str, Any], required: bool) -> Dict[str, Any]:
    if provided:
        record = _build_new_consent_record(consent_type, provided, payload, required)
        save_consent_record(customer_id, record)
        return record

    reusable = _find_reusable_consent(customer_id, consent_type)
    if reusable:
        reused = dict(reusable)
        reused["reused"] = True
        reused["status"] = _derive_record_status(reused)
        reused["is_expired"] = reused["status"] == "expired"
        return reused

    return _build_new_consent_record(consent_type, False, payload, required)


def _evaluate_consent(context: OrchestrationContext, payload: Dict[str, Any]) -> Dict[str, Any]:
    processing_provided = bool(payload.get("processingConsent", False))
    disclosure_provided = bool(payload.get("disclosureConsent", False))

    processing_record = _get_or_create_consent_record(context.customer_id, "processing", processing_provided, payload, True)
    disclosure_record = _get_or_create_consent_record(context.customer_id, "disclosure", disclosure_provided, payload, context.disclose_to_third_party)

    consent_records = [processing_record, disclosure_record]

    status = "pass" if all((not r["required"]) or r["status"] == "valid" for r in consent_records) else "fail"

    reasons: List[str] = []
    for record in consent_records:
        if not record["required"]:
            continue
        if record["status"] == "missing":
            reasons.append(f"{record['consent_type']}_consent_missing")
        elif record["status"] == "invalid":
            reasons.append(f"{record['consent_type']}_consent_invalid")
        elif record["status"] == "expired":
            reasons.append(f"{record['consent_type']}_consent_expired")
        elif record["status"] == "revoked":
            reasons.append(f"{record['consent_type']}_consent_revoked")

    return {
        "processing_consent_required": True,
        "disclosure_consent_required": context.disclose_to_third_party,
        "status": status,
        "reasons": reasons,
        "mode": ENFORCEMENT_MODE,
        "consent_records": consent_records,
    }


def _infer_document_type(document_id: str) -> str:
    normalized = document_id.strip().lower()
    if "bank" in normalized or "statement" in normalized:
        return "bank_statement"
    if "id" in normalized or "identity" in normalized:
        return "identity_document"
    if "address" in normalized or "poa" in normalized or "proof" in normalized:
        return "proof_of_address"
    return "unknown"


def _assess_document(document_id: str, expected_types: set[str]) -> Dict[str, Any]:
    inferred_type = _infer_document_type(document_id)
    quality_status = "acceptable" if len(document_id.strip()) >= 6 else "poor"
    freshness_status = "unknown"
    completeness_status = "unknown"

    reasons: List[str] = []
    readiness_score = 100

    if inferred_type == "unknown":
        reasons.append("document_type_unknown")
        readiness_score -= 30

    if inferred_type not in expected_types and inferred_type != "unknown":
        reasons.append("document_type_not_expected_for_service")
        readiness_score -= 20

    if quality_status != "acceptable":
        reasons.append("document_identifier_quality_poor")
        readiness_score -= 20

    if inferred_type in {"bank_statement", "identity_document", "proof_of_address"}:
        completeness_status = "assumed_present"
    else:
        completeness_status = "unknown"

    readiness_score = max(0, readiness_score)
    status = "pass" if readiness_score >= 70 and "document_type_not_expected_for_service" not in reasons else "fail"

    return {
        "document_id": document_id,
        "inferred_type": inferred_type,
        "expected_for_service": inferred_type in expected_types,
        "quality_status": quality_status,
        "freshness_status": freshness_status,
        "completeness_status": completeness_status,
        "readiness_score": readiness_score,
        "status": status,
        "reasons": reasons,
    }


def _evaluate_documents(context: OrchestrationContext) -> Dict[str, Any]:
    expected_types = EXPECTED_DOCUMENT_TYPES.get(context.service_family, set())
    assessments = [_assess_document(doc_id, expected_types) for doc_id in context.document_ids]

    reasons: List[str] = []
    if not context.document_ids:
        reasons.append("documents_missing")

    supplied_types = {a["inferred_type"] for a in assessments if a["inferred_type"] != "unknown"}
    missing_expected_types = sorted(list(expected_types - supplied_types))
    if missing_expected_types:
        reasons.append("required_document_types_missing")

    failing_docs = [a for a in assessments if a["status"] == "fail"]
    avg_score = int(sum(a["readiness_score"] for a in assessments) / len(assessments)) if assessments else 0
    overall_status = "pass" if not reasons and not failing_docs and avg_score >= 70 else "fail"

    return {
        "document_ids_received": context.document_ids,
        "document_count": len(context.document_ids),
        "assessments": assessments,
        "expected_document_types": sorted(list(expected_types)),
        "missing_expected_document_types": missing_expected_types,
        "average_readiness_score": avg_score,
        "status": overall_status,
        "reasons": reasons,
        "mode": ENFORCEMENT_MODE,
    }


def _build_enforcement(consent_check: Dict[str, Any], document_check: Dict[str, Any]) -> Dict[str, Any]:
    overall = "pass" if consent_check["status"] == "pass" and document_check["status"] == "pass" else "fail"
    return {
        "consent": consent_check,
        "documents": document_check,
        "overall_status": overall,
        "enforcement_mode": ENFORCEMENT_MODE,
        "blocks_execution": ENFORCEMENT_MODE == "hard",
    }


def _build_remediation_prompts(enforcement: Dict[str, Any]) -> List[Dict[str, str]]:
    prompts: List[Dict[str, str]] = []

    for reason in enforcement["consent"]["reasons"]:
        mapping = {
            "processing_consent_missing": "Capture valid processing consent before execution.",
            "disclosure_consent_missing": "Capture valid disclosure consent before third-party sharing.",
            "processing_consent_invalid": "Provide valid processing consent evidence reference and source.",
            "disclosure_consent_invalid": "Provide valid disclosure consent evidence reference and source.",
            "processing_consent_expired": "Refresh expired processing consent before execution.",
            "disclosure_consent_expired": "Refresh expired disclosure consent before sharing.",
            "processing_consent_revoked": "Capture a new processing consent because the previous one was revoked.",
            "disclosure_consent_revoked": "Capture a new disclosure consent because the previous one was revoked.",
        }
        if reason in mapping:
            prompts.append({"reason": reason, "suggestedAction": mapping[reason]})

    for reason in enforcement["documents"]["reasons"]:
        if reason == "documents_missing":
            prompts.append({"reason": reason, "suggestedAction": "Upload the required documents before execution."})
        elif reason == "required_document_types_missing":
            missing = enforcement["documents"].get("missing_expected_document_types", [])
            prompts.append({
                "reason": reason,
                "suggestedAction": f"Provide missing document types required for this service: {', '.join(missing)}.",
            })

    for assessment in enforcement["documents"].get("assessments", []):
        for reason in assessment.get("reasons", []):
            if reason == "document_type_unknown":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Clarify or relabel document {assessment['document_id']} so its type can be identified.",
                })
            elif reason == "document_type_not_expected_for_service":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Replace document {assessment['document_id']} with one expected for this service.",
                })
            elif reason == "document_identifier_quality_poor":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Improve document identifier or source quality for {assessment['document_id']}.",
                })

    deduped: List[Dict[str, str]] = []
    seen = set()
    for prompt in prompts:
        key = (prompt["reason"], prompt["suggestedAction"])
        if key not in seen:
            seen.add(key)
            deduped.append(prompt)
    return deduped


def _execution_mode() -> str:
    return os.getenv("EXECUTION_MODE", "local").strip().lower()


def _resolve_downstream_target(service_family: str) -> Dict[str, Any]:
    targets = {
        "financial_management": {
            "target_type": "ecs",
            "cluster": "ocr-rebuild-cluster",
            "task_definition": "financial-management-worker-task-prod",
            "container_name": "financial_management",
        },
        "fica": {
            "target_type": "ecs",
            "cluster": "ocr-rebuild-cluster",
            "task_definition": "fica-compliance-worker-task-prod",
            "container_name": "fica_compliance",
        },
        "credit_decision": {
            "target_type": "ecs",
            "cluster": "ocr-rebuild-cluster",
            "task_definition": "credit-decision-worker-task-prod",
            "container_name": "credit_decision",
        },
    }
    if service_family not in targets:
        raise ValueError(f"Unsupported service_family for downstream target: {service_family}")
    return targets[service_family]


def _build_execution_plan(context: OrchestrationContext, execution_mode: str) -> Dict[str, Any]:
    downstream_target = _resolve_downstream_target(context.service_family)

    stages = [
        {
            "stage_id": "consent_check",
            "stage_order": 10,
            "stage_type": "validation",
            "required": True,
            "blocking": True,
            "status": "pending",
            "target": {
                "target_type": "internal",
                "callable": "_evaluate_consent",
            },
            "inputs": {
                "input_source": "request_payload",
                "payload_builder": None,
                "depends_on": [],
            },
            "outputs": {
                "result_key": "consent_check",
                "persist": True,
            },
            "failure_policy": {
                "on_fail": "stop_plan",
                "result_status": "blocked",
            },
        },
        {
            "stage_id": "document_check",
            "stage_order": 20,
            "stage_type": "validation",
            "required": True,
            "blocking": True,
            "status": "pending",
            "target": {
                "target_type": "internal",
                "callable": "_evaluate_documents",
            },
            "inputs": {
                "input_source": "request_context",
                "payload_builder": None,
                "depends_on": [],
            },
            "outputs": {
                "result_key": "document_check",
                "persist": True,
            },
            "failure_policy": {
                "on_fail": "stop_plan",
                "result_status": "blocked",
            },
        },
        {
            "stage_id": "enforcement_decision",
            "stage_order": 30,
            "stage_type": "decision",
            "required": True,
            "blocking": True,
            "status": "pending",
            "target": {
                "target_type": "internal",
                "callable": "_build_enforcement",
            },
            "inputs": {
                "input_source": "prior_stage_results",
                "payload_builder": None,
                "depends_on": ["consent_check", "document_check"],
            },
            "outputs": {
                "result_key": "enforcement",
                "persist": True,
            },
            "failure_policy": {
                "on_fail": "stop_plan",
                "result_status": "blocked",
            },
        },
        {
            "stage_id": "downstream_execution",
            "stage_order": 40,
            "stage_type": "execution",
            "required": True,
            "blocking": False,
            "status": "pending",
            "target": downstream_target,
            "inputs": {
                "input_source": "execution_payload",
                "payload_builder": "request_execution_payload_v1",
                "depends_on": ["enforcement_decision"],
            },
            "outputs": {
                "result_key": "downstream_execution",
                "persist": True,
            },
            "failure_policy": {
                "on_fail": "mark_execution_failed",
                "result_status": "execution_failed",
            },
        },
        {
            "stage_id": "result_finalize",
            "stage_order": 50,
            "stage_type": "finalization",
            "required": True,
            "blocking": False,
            "status": "pending",
            "target": {
                "target_type": "internal",
                "callable": "_finalize_result_record",
            },
            "inputs": {
                "input_source": "prior_stage_results",
                "payload_builder": None,
                "depends_on": ["enforcement_decision", "downstream_execution"],
            },
            "outputs": {
                "result_key": "finalization",
                "persist": True,
            },
            "failure_policy": {
                "on_fail": "mark_execution_failed",
                "result_status": "execution_failed",
            },
        },
    ]

    plan_runtime_lock = None
    if context.service_family == "financial_management":
        plan_runtime_lock = _resolve_financial_management_runtime_lock(
            context.analysis_type or "explain_document"
        )

    return {
        "plan_id": _new_plan_id(context.request_id),
        "request_id": context.request_id,
        "service_family": context.service_family,
        "service_code": context.service_code,
        "plan_version": "execution_plan_v1",
        "governed_runtime_lock": plan_runtime_lock,
        "execution_mode": execution_mode,
        "created_at": _utc_now(),
        "plan_status": "pending",
        "stages": stages,
        "finalization": {
            "persist_request_record": True,
            "persist_stage_results": True,
            "generate_remediation_prompts": True,
        },
        "plan_summary": {
            "blocking_stage_count": sum(1 for s in stages if s["blocking"]),
            "required_stage_count": sum(1 for s in stages if s["required"]),
            "execution_stage_count": sum(1 for s in stages if s["stage_type"] == "execution"),
        },
    }


def _set_stage_status(plan: Dict[str, Any], stage_id: str, status: str) -> None:
    for stage in plan["stages"]:
        if stage["stage_id"] == stage_id:
            stage["status"] = status
            return
    raise ValueError(f"Stage not found in plan: {stage_id}")


def _mark_remaining_stages(plan: Dict[str, Any], after_stage_id: str, status: str) -> None:
    seen = False
    for stage in plan["stages"]:
        if seen and stage["status"] == "pending":
            stage["status"] = status
        if stage["stage_id"] == after_stage_id:
            seen = True


def _execute(
    context: OrchestrationContext,
    execution_plan: Dict[str, Any],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    execution_payload = {
        "request_id": context.request_id,
        "customer_id": context.customer_id,
        "service_code": context.service_code,
        "service_family": context.service_family,
        "document_ids": context.document_ids,
        "disclose_to_third_party": context.disclose_to_third_party,
        "timestamp": _utc_now(),
        "transactions": payload.get("transactions"),
        "document_metadata": payload.get("document_metadata"),
        "multi_period_requirement_signal": payload.get("multi_period_requirement_signal"),
        "prior_statement_history": payload.get("prior_statement_history"),
        "governed_runtime_lock": execution_plan.get("governed_runtime_lock"),
        "execution_plan": execution_plan,
        "orchestration_context": {
            "plan_id": execution_plan.get("plan_id"),
            "plan_version": execution_plan.get("plan_version"),
            "current_stage": "downstream_execution",
            "plan_status": execution_plan.get("plan_status"),
        },
    }
    return execute_service_family(context.service_family, execution_payload)


def _finalize_result_record(
    plan: Dict[str, Any],
    enforcement: Dict[str, Any],
    downstream_execution: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    if enforcement["overall_status"] != "pass":
        return {
            "request_status": "blocked",
            "result_status": "blocked",
            "plan_status": "blocked",
            "finalization_reason": "pre_execution_enforcement_failed",
        }

    worker_status = None
    invocation_result = None
    runtime_lock = plan.get("governed_runtime_lock")

    if downstream_execution:
        execution = downstream_execution.get("execution", {}) or {}
        invocation_result = execution.get("invocation", {}).get("result")

        if not isinstance(invocation_result, dict):
            invocation_result = (
                execution.get("fallback", {})
                .get("invocation", {})
                .get("result")
            )

        if isinstance(invocation_result, dict):
            worker_status = invocation_result.get("status")

    if worker_status == "executed":
        if runtime_lock:
            result_payload = invocation_result.get("result") if isinstance(invocation_result, dict) else None
            expected_outcome_result_key = runtime_lock.get("outcome_result_key")
            outcome_block = result_payload.get(expected_outcome_result_key) if isinstance(result_payload, dict) else None

            if plan.get("service_code") != runtime_lock.get("service_code"):
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_service_code_mismatch",
                }

            if plan.get("service_family") != runtime_lock.get("service_family"):
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_service_family_mismatch",
                }

            if not isinstance(result_payload, dict):
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_result_missing",
                }

            outcome_keys = sorted([k for k in result_payload.keys() if k.startswith("fm_otc_")])
            if outcome_keys != [expected_outcome_result_key]:
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_governed_outcome_mismatch",
                }

            allowed_outcome_codes = {
                cfg["governed_outcome_code"] for cfg in FM_GOVERNED_RUNTIME_LOCKS.values()
            }
            if runtime_lock.get("governed_outcome_code") not in allowed_outcome_codes:
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_governed_outcome_code_invalid",
                }

            if not isinstance(outcome_block, dict):
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_outcome_block_missing",
                }

            if outcome_block.get("outcome_intent") != runtime_lock.get("outcome_intent"):
                return {
                    "request_status": "completed",
                    "result_status": "execution_failed",
                    "plan_status": "failed",
                    "finalization_reason": "runtime_lock_outcome_intent_mismatch",
                }

        return {
            "request_status": "completed",
            "result_status": "available",
            "plan_status": "completed",
            "finalization_reason": "downstream_execution_succeeded",
        }

    if worker_status == "rejected":
        return {
            "request_status": "completed",
            "result_status": "rejected",
            "plan_status": "failed",
            "finalization_reason": "downstream_worker_rejected_payload",
        }

    return {
        "request_status": "completed",
        "result_status": "execution_failed",
        "plan_status": "failed",
        "finalization_reason": "downstream_execution_failed",
    }


def _execute_plan(
    plan: Dict[str, Any],
    context: OrchestrationContext,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    stage_results: Dict[str, Any] = {}
    plan["plan_status"] = "running"

    _set_stage_status(plan, "consent_check", "running")
    consent_check = _evaluate_consent(context, payload)
    stage_results["consent_check"] = consent_check
    _set_stage_status(plan, "consent_check", "passed" if consent_check["status"] == "pass" else "failed")

    _set_stage_status(plan, "document_check", "running")
    document_check = _evaluate_documents(context)
    stage_results["document_check"] = document_check
    _set_stage_status(plan, "document_check", "passed" if document_check["status"] == "pass" else "failed")

    _set_stage_status(plan, "enforcement_decision", "running")
    enforcement = _build_enforcement(consent_check, document_check)
    stage_results["enforcement_decision"] = enforcement

    if enforcement["overall_status"] != "pass":
        _set_stage_status(plan, "enforcement_decision", "failed")
        _mark_remaining_stages(plan, "enforcement_decision", "blocked")
        finalization = _finalize_result_record(plan, enforcement, None)
        stage_results["result_finalize"] = finalization
        plan["plan_status"] = finalization["plan_status"]
        return {
            "plan": plan,
            "stage_results": stage_results,
            "consent_check": consent_check,
            "document_check": document_check,
            "enforcement": enforcement,
            "downstream_execution": None,
            "finalization": finalization,
        }

    _set_stage_status(plan, "enforcement_decision", "passed")

    _set_stage_status(plan, "downstream_execution", "running")
    downstream_execution = _execute(context, plan, payload)
    stage_results["downstream_execution"] = downstream_execution

    execution = downstream_execution.get("execution", {}) or {}
    invocation_result = execution.get("invocation", {}).get("result")

    if not isinstance(invocation_result, dict):
        invocation_result = (
            execution.get("fallback", {})
            .get("invocation", {})
            .get("result")
        )

    worker_status = invocation_result.get("status") if isinstance(invocation_result, dict) else None

    if worker_status == "executed":
        _set_stage_status(plan, "downstream_execution", "completed")
    else:
        _set_stage_status(plan, "downstream_execution", "failed")

    _set_stage_status(plan, "result_finalize", "running")
    finalization = _finalize_result_record(plan, enforcement, downstream_execution)
    stage_results["result_finalize"] = finalization
    _set_stage_status(plan, "result_finalize", "completed")
    plan["plan_status"] = finalization["plan_status"]

    return {
        "plan": plan,
        "stage_results": stage_results,
        "consent_check": consent_check,
        "document_check": document_check,
        "enforcement": enforcement,
        "downstream_execution": downstream_execution,
        "finalization": finalization,
    }


def get_catalog() -> Dict[str, Any]:
    items = [
        {"serviceCode": "financial_management", "serviceName": "Financial Management", "serviceFamily": "financial_management", "requiresProcessingConsent": True, "requiresDisclosureConsent": False},
        {"serviceCode": "fica", "serviceName": "FICA Compliance", "serviceFamily": "fica", "requiresProcessingConsent": True, "requiresDisclosureConsent": False},
        {"serviceCode": "credit_decision", "serviceName": "Credit Decision", "serviceFamily": "credit_decision", "requiresProcessingConsent": True, "requiresDisclosureConsent": True},
    ]
    return _base_response(success=True, status="ready", message="Service catalog retrieved.", data={"items": items})


def create_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    context = _build_context(payload)
    execution_plan = _build_execution_plan(context, _execution_mode())

    plan_execution = _execute_plan(execution_plan, context, payload)
    execution_plan = plan_execution["plan"]
    stage_results = plan_execution["stage_results"]
    consent_check = plan_execution["consent_check"]
    document_check = plan_execution["document_check"]
    enforcement = plan_execution["enforcement"]
    downstream_execution = plan_execution["downstream_execution"]
    finalization = plan_execution["finalization"]

    remediation_prompts = _build_remediation_prompts(enforcement)

    orchestration_record = {
        "request": asdict(context),
        "execution_plan": execution_plan,
        "stage_results": stage_results,
        "consent_check": consent_check,
        "consent_records": consent_check["consent_records"],
        "document_check": document_check,
        "enforcement": enforcement,
        "remediation_prompts": remediation_prompts,
        "routing": {
            "selected_service_family": context.service_family,
            "selected_service_code": context.service_code,
            "orchestration_layer": "services.decision_engine.frontend_request_orchestrator",
        },
        "request_status": finalization["request_status"],
        "result_status": finalization["result_status"],
        "finalization_reason": finalization["finalization_reason"],
        "downstream_execution": downstream_execution,
        "last_updated": _utc_now(),
    }

    save_request(orchestration_record)

    if finalization["request_status"] == "blocked":
        return _base_response(
            success=False,
            status="blocked_by_enforcement",
            message="Request blocked due to failed pre-execution checks.",
            data=orchestration_record,
        )

    return _base_response(
        success=True,
        status="executed",
        message="Request evaluated, executed, and persisted under hard enforcement.",
        data=orchestration_record,
    )


def get_status(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(success=False, status="not_found", message="Request status not found.", data={"requestId": request_id})

    return _base_response(
        success=True,
        status="ready",
        message="Request status retrieved.",
        data={
            "requestId": request_id,
            "requestStatus": record.get("request_status", "unknown"),
            "resultStatus": record.get("result_status", "unknown"),
            "finalizationReason": record.get("finalization_reason"),
            "serviceFamily": record["request"]["service_family"],
            "enforcementOverallStatus": record.get("enforcement", {}).get("overall_status"),
            "documentReadinessScore": record.get("document_check", {}).get("average_readiness_score"),
            "consentRecords": record.get("consent_records", []),
            "lastUpdated": record.get("last_updated"),
        },
    )


def get_remediation(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(success=False, status="not_found", message="Remediation prompts not found.", data={"requestId": request_id})

    return _base_response(
        success=True,
        status="ready",
        message="Remediation prompts retrieved.",
        data={"requestId": request_id, "prompts": record.get("remediation_prompts", [])},
    )


def get_result(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(success=False, status="not_found", message="Result not found.", data={"requestId": request_id})

    return _base_response(
        success=True,
        status="ready",
        message="Request result retrieved.",
        data={
            "requestId": request_id,
            "requestStatus": record.get("request_status", "unknown"),
            "resultStatus": record.get("result_status", "unknown"),
            "finalizationReason": record.get("finalization_reason"),
            "result": record.get("downstream_execution"),
            "enforcement": record.get("enforcement"),
        },
    )


def rerun_request(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(success=False, status="not_found", message="Request not found for rerun.", data={"requestId": request_id})

    context_payload = {
        "customerId": record["request"]["customer_id"],
        "serviceCode": record["request"]["service_code"],
        "documentIds": record["request"]["document_ids"],
        "discloseToThirdParty": record["request"]["disclose_to_third_party"],
        "processingConsent": True,
        "processingConsentSource": "rerun",
        "processingConsentEvidenceRef": "rerun_processing_consent",
        "disclosureConsent": record["request"]["disclose_to_third_party"],
        "disclosureConsentSource": "rerun" if record["request"]["disclose_to_third_party"] else None,
        "disclosureConsentEvidenceRef": "rerun_disclosure_consent" if record["request"]["disclose_to_third_party"] else None,
    }

    rerun_response = create_request(context_payload)
    return _base_response(
        success=rerun_response["success"],
        status=rerun_response["status"],
        message="Request rerun attempted.",
        data={
            "originalRequestId": request_id,
            "rerunResponse": rerun_response["data"],
        },
    )
