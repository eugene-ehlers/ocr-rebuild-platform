# Translation — Capability v1

## Purpose
Provide language detection and multi-language translation support for financial documents.

## Inputs
- raw_text
- language_code (optional if detected)
- document_type

## Processing Logic
- Detect language
- Translate to target language(s)
- Maintain structural and table integrity
- Assign confidence per translation

## Outputs
{
  "translated_text": "string",
  "metadata": {
    "source_language": "string",
    "target_language": "string",
    "confidence": 0.90
  }
}

## Failure Modes
- Language not detected
- OCR errors propagate
- Translation API failures

## Dependencies
- OCR output
- Layout understanding
- Optional previous translations

## Cost Consideration
- External API cost if using cloud translation
- Medium compute for large documents

## Why this capability is critical
Enables cross-language support and consistent customer-facing insights.
