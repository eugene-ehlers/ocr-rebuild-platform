# I-DIP results callback

When the OCR worker finishes extraction it must call:

```
POST {IDIP_RESULTS_BASE_URL}/my/passport/documents/ocr-result/{document_id}
Content-Type: application/json

{
  "raw_ocr_text": "full extracted text",
  "fields": {
    "gross_monthly": "15000",
    "payer": "Example Employer"
  }
}
```

Environment:
- `IDIP_RESULTS_BASE_URL` — base URL of the I-DIP app (e.g. http://127.0.0.1:8092 on the Passport host).

I-DIP stores `raw_ocr_text` permanently and uses `fields` to pre-fill the matching form for user review.

Helper: `services/decision_engine/idip_results_callback.py` → `post_results(...)`.
