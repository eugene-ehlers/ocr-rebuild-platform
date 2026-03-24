from __future__ import annotations

from io import BytesIO
from typing import Any, Dict

import pytesseract
from PIL import Image

from services.ocr.providers.base_provider import OCRProviderAdapter


class TesseractProviderAdapter(OCRProviderAdapter):
    provider_name = "tesseract"
    provider_type = "open_source"

    def execute(self, image_bytes: bytes, provider_instruction: Dict[str, Any]) -> Dict[str, Any]:
        if bool(provider_instruction.get("proof_force_primary_failure", False)):
            raise RuntimeError("controlled_primary_failure_for_governed_live_fallback_proof_v1")

        with Image.open(BytesIO(image_bytes)) as img:
            text = pytesseract.image_to_string(img).strip()

        confidence = 0.0 if not text else 0.75

        return {
            "status": "completed",
            "text": text,
            "confidence": confidence,
            "provider": provider_instruction["provider"],
            "provider_type": provider_instruction["provider_type"],
            "engine_name": "tesseract",
            "engine_version": "provider_contract_v1",
            "provider_metadata": {
                "execution_mode": provider_instruction["execution_mode"],
                "decision_reason": provider_instruction["decision_reason"],
            },
            "error": None,
        }
