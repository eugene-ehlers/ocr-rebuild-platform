from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class OCRProviderAdapter(ABC):
    """
    Governed OCR provider adapter interface.

    Adapters execute provider-specific OCR behavior only.
    They must not own provider selection or fallback decisions.
    """

    provider_name: str = ""
    provider_type: str = ""

    @abstractmethod
    def execute(self, image_bytes: bytes, provider_instruction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute OCR for the supplied provider instruction and return a
        normalized provider result structure.
        """
        raise NotImplementedError
