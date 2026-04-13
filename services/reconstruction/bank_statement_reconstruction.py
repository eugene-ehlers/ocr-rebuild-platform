from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

DATE_PATTERNS = [
    re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b"),
    re.compile(r"\b(\d{2})-(\d{2})-(\d{4})\b"),
    re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"),
    re.compile(r"\b(\d{2})/(\d{2})\b"),
    re.compile(r"\b(\d{2})-(\d{2})\b"),
]

MONEY_PATTERN = re.compile(r"[-+]?\d[\d,]*\.\d{2}")

RECONSTRUCTION_MODEL_ID = "bank_reconstruction_champion_v1_13Apr2026"


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _normalize_date(raw: str) -> Optional[str]:
    text = str(raw or "").strip()
    if not text:
        return None

    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue

        groups = match.groups()
        if len(groups) == 3 and len(groups[0]) == 4:
            year, month, day = groups
            return f"{year}-{month}-{day}"
        if len(groups) == 3:
            day, month, year = groups
            return f"{year}-{month}-{day}"
        if len(groups) == 2:
            day, month = groups
            return f"2026-{month}-{day}"

    return None


def _parse_money(raw: str) -> Optional[float]:
    text = str(raw or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _extract_amounts(line: str) -> List[float]:
    amounts: List[float] = []
    for token in MONEY_PATTERN.findall(line or ""):
        value = _parse_money(token)
        if value is not None:
            amounts.append(value)
    return amounts


def _infer_type_and_amount(amounts: List[float], line: str) -> Optional[Dict[str, Any]]:
    if not amounts:
        return None

    lowered = str(line or "").lower()
    primary = amounts[0]

    txn_type = "credit" if primary > 0 else "debit"
    amount = abs(primary)

    if any(token in lowered for token in ["cr ", " credit", "deposit", "salary", "payroll", "wage", "inflow"]):
        txn_type = "credit"
    if any(token in lowered for token in ["db ", " debit", "pos", "purchase", "wdl", "withdrawal", "atm", "fee", "charge", "debit order"]):
        txn_type = "debit"

    balance = abs(amounts[-1]) if len(amounts) >= 2 else None

    return {
        "type": txn_type,
        "amount": round(amount, 2),
        "balance": round(balance, 2) if balance is not None else None,
    }


def _clean_description(line: str, date_text: Optional[str], amounts: List[float]) -> str:
    text = str(line or "")
    if date_text:
        text = text.replace(date_text, " ")
    for token in MONEY_PATTERN.findall(line or ""):
        text = text.replace(token, " ")
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text


def parse_transaction_line(line: str) -> Optional[Dict[str, Any]]:
    raw = str(line or "").strip()
    if not raw:
        return None

    date_text = None
    normalized_date = None
    for pattern in DATE_PATTERNS:
        match = pattern.search(raw)
        if match:
            date_text = match.group(0)
            normalized_date = _normalize_date(date_text)
            break

    amounts = _extract_amounts(raw)
    amount_info = _infer_type_and_amount(amounts, raw)

    if not normalized_date or not amount_info:
        return None

    description = _clean_description(raw, date_text, amounts)
    if not description:
        return None

    return {
        "transaction_date": normalized_date,
        "date": normalized_date,
        "description": description,
        "amount": amount_info["amount"],
        "type": amount_info["type"],
        "balance": amount_info["balance"],
        "confidence": 0.70,
        "source": "ocr_reconstruction_v1",
        "reconstruction_model_id": RECONSTRUCTION_MODEL_ID,
        "raw_line": raw,
    }


def reconstruct_transactions_from_pages(pages: Any) -> List[Dict[str, Any]]:
    transactions: List[Dict[str, Any]] = []
    for page in _safe_list(pages):
        text = str(_safe_dict(page).get("extracted_text") or "")
        for line in text.splitlines():
            parsed = parse_transaction_line(line)
            if parsed:
                transactions.append(parsed)
    return transactions


def build_bank_statement_structured_from_pages(pages: Any) -> Dict[str, Any]:
    transactions = reconstruct_transactions_from_pages(pages)
    dates = [t.get("date") for t in transactions if t.get("date")]
    return {
        "transactions": transactions,
        "transaction_count": len(transactions),
        "statement_period_start": min(dates) if dates else None,
        "statement_period_end": max(dates) if dates else None,
        "reconstruction_method": "ocr_reconstruction_v1",
        "reconstruction_model_id": RECONSTRUCTION_MODEL_ID,
    }


def get_or_reconstruct_bank_statement_structured(payload: Dict[str, Any]) -> Dict[str, Any]:
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured_fields = _safe_dict(ocr.get("structured_fields"))
    bank_statement = _safe_dict(structured_fields.get("bank_statement"))
    if bank_statement.get("transactions"):
        return bank_statement
    pages = _safe_list(ocr.get("pages"))
    if pages:
        return build_bank_statement_structured_from_pages(pages)
    return {}


def enrich_payload_for_bank_statement_contract(payload: Dict[str, Any]) -> Dict[str, Any]:
    enriched = dict(payload)

    document = _safe_dict(enriched.get("document"))
    doc_ids = _safe_list(enriched.get("document_ids"))
    if not document.get("document_id") and doc_ids:
        document["document_id"] = str(doc_ids[0])
    if not document.get("document_type"):
        document["document_type"] = "bank_statement"
    if not document.get("file_format"):
        document["file_format"] = "json"
    enriched["document"] = document

    request = _safe_dict(enriched.get("request"))
    if not request.get("outcome_code"):
        request["outcome_code"] = enriched.get("governed_outcome_code")
    if not request.get("manifest_id"):
        request["manifest_id"] = enriched.get("manifest_id")
    enriched["request"] = request

    return enriched


def enrich_ocr_contract_from_pages(payload: Dict[str, Any]) -> Dict[str, Any]:
    enriched = dict(payload)

    substrates = _safe_dict(enriched.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    pages = _safe_list(ocr.get("pages"))

    if not ocr.get("raw_text") and pages:
        ocr["raw_text"] = "\n".join(str(p.get("extracted_text") or "") for p in pages)

    if not ocr.get("page_traces") and pages:
        ocr["page_traces"] = [
            {"page_number": p.get("page_number"), "status": "processed"}
            for p in pages
        ]

    if not ocr.get("engine_metadata"):
        ocr["engine_metadata"] = {
            "engine": "ocr_reconstruction_v1",
            "provider": "internal",
            "confidence_proxy": 0.7,
        }

    substrates["ocr"] = ocr
    enriched["substrates"] = substrates

    return enriched
