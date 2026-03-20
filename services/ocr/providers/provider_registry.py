from __future__ import annotations

import os

from typing import Dict, List

from services.ocr.providers.base_provider import OCRProviderAdapter
from services.ocr.providers.tesseract_provider import TesseractProviderAdapter
from services.ocr.providers.aws_textract_provider import (
    AwsTextractDetectDocumentTextProviderAdapter,
)


SUPPORTED_PROVIDERS: Dict[str, Dict[str, object]] = {
    "tesseract": {
        "provider_type": "open_source",
        "execution_modes": {"primary", "fallback", "recovery"},
        "runtime_enabled": True,
    },
    "aws_textract_detect_document_text": {
        "provider_type": "managed_service",
        "execution_modes": {"primary", "fallback", "recovery"},
        "runtime_enabled": os.environ.get("ENABLE_AWS_TEXTRACT_PROVIDER", "false").strip().lower() == "true",
    },
}

PROVIDER_ADAPTERS: Dict[str, OCRProviderAdapter] = {
    "tesseract": TesseractProviderAdapter(),
    "aws_textract_detect_document_text": AwsTextractDetectDocumentTextProviderAdapter(),
}


def get_supported_provider_config(provider_name: str) -> Dict[str, object]:
    return dict(SUPPORTED_PROVIDERS.get(provider_name, {}))


def get_runtime_enabled_providers() -> List[str]:
    return [
        provider_name
        for provider_name, config in SUPPORTED_PROVIDERS.items()
        if bool(config.get("runtime_enabled", False))
    ]


def is_provider_runtime_enabled(provider_name: str) -> bool:
    config = get_supported_provider_config(provider_name)
    return bool(config.get("runtime_enabled", False))
