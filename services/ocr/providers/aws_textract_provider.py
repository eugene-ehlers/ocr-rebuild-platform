from __future__ import annotations

from typing import Any, Dict, List

import boto3

from services.ocr.providers.base_provider import OCRProviderAdapter


class AwsTextractDetectDocumentTextProviderAdapter(OCRProviderAdapter):
    provider_name = "aws_textract_detect_document_text"
    provider_type = "managed_service"

    def __init__(self) -> None:
        self._textract = boto3.client("textract")

    def execute(self, image_bytes: bytes, provider_instruction: Dict[str, Any]) -> Dict[str, Any]:
        response = self._textract.detect_document_text(
            Document={"Bytes": image_bytes}
        )

        text_lines: List[str] = []
        confidence_values: List[float] = []

        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE":
                text = str(block.get("Text", "")).strip()
                if text:
                    text_lines.append(text)
                try:
                    confidence_values.append(float(block.get("Confidence", 0.0)) / 100.0)
                except Exception:
                    confidence_values.append(0.0)

        average_confidence = (
            sum(confidence_values) / len(confidence_values)
            if confidence_values
            else 0.0
        )

        return {
            "status": "completed",
            "text": "\n".join(text_lines).strip(),
            "confidence": average_confidence,
            "provider": provider_instruction["provider"],
            "provider_type": provider_instruction["provider_type"],
            "engine_name": "aws_textract_detect_document_text",
            "engine_version": "provider_contract_v1",
            "provider_metadata": {
                "execution_mode": provider_instruction["execution_mode"],
                "decision_reason": provider_instruction["decision_reason"],
            },
            "error": None,
            "raw_provider_summary": {
                "block_count": len(response.get("Blocks", [])),
                "document_metadata": response.get("DocumentMetadata", {}),
            },
        }
