import io
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
import importlib.util

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, relative_path: str):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_test_image_bytes():
    img = Image.new("RGB", (20, 20), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    manifest_mod = load_module("manifest_generator", "services/manifest_generator/lambda_function.py")
    preprocessing_mod = load_module("preprocessing", "services/preprocessing/lambda_function.py")
    ocr_mod = load_module("ocr_worker", "services/ocr/ocr_worker.py")
    table_mod = load_module("table_worker", "services/table_extraction/table_worker.py")
    logo_mod = load_module("logo_worker", "services/logo_recognition/logo_worker.py")
    fraud_mod = load_module("fraud_worker", "services/fraud_detection/fraud_worker.py")
    aggregation_mod = load_module("aggregation_worker", "services/aggregation/aggregation_worker.py")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Manifest
        with patch.object(manifest_mod, "save_manifest", return_value={"status": "saved", "manifest_id": "UNKNOWN"}):
            manifest_result = manifest_mod.lambda_handler(
                {
                    "document_id": "doc-1",
                    "source_uri": "s3://bucket/file.pdf",
                    "pages": [{"page_number": 1, "s3_key": "uploads/page1.png"}]
                },
                None
            )

        # Preprocessing
        test_bytes = make_test_image_bytes()

        class MockBody:
            def read(self):
                return test_bytes

        class MockPreprocessS3:
            def get_object(self, Bucket, Key):
                return {"Body": MockBody()}

            def put_object(self, Bucket, Key, Body, ContentType):
                pass

        with patch.object(preprocessing_mod, "s3", MockPreprocessS3()):
            preprocessing_result = preprocessing_mod.lambda_handler(
                {
                    "document_id": "doc-1",
                    "source_uri": "s3://bucket/file.pdf",
                    "source_bucket": "source-bucket",
                    "pages": [{"page_number": 1, "s3_key": "uploads/page1.png"}]
                },
                None
            )

        # OCR via file contract
        ocr_input = tmpdir / "ocr_input.json"
        ocr_output = tmpdir / "ocr_output.json"
        ocr_input.write_text(json.dumps(preprocessing_result), encoding="utf-8")

        class MockOcrS3:
            def get_object(self, Bucket, Key):
                return {"Body": MockBody()}

        with patch.object(ocr_mod, "s3", MockOcrS3()):
            with patch.object(
                ocr_mod.pytesseract,
                "image_to_string",
                return_value="Tax Invoice\nInvoice Number: 12345\nname | age\njohn | 30\nmary | 25"
            ):
                with patch.dict(os.environ, {"OCR_INPUT": str(ocr_input), "OCR_OUTPUT": str(ocr_output)}):
                    ocr_mod.OCR_INPUT = str(ocr_input)
                    ocr_mod.OCR_OUTPUT = str(ocr_output)
                    ocr_mod.main()

        ocr_result = json.loads(ocr_output.read_text(encoding="utf-8"))

        # Table extraction
        table_input = tmpdir / "table_input.json"
        table_output = tmpdir / "table_output.json"
        table_input.write_text(json.dumps({
            "document_id": ocr_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": ocr_result["source_uri"],
            "pages": ocr_result["pages"]
        }), encoding="utf-8")

        with patch.dict(os.environ, {
            "TABLE_EXTRACTION_INPUT": str(table_input),
            "TABLE_EXTRACTION_OUTPUT": str(table_output)
        }):
            table_mod.main()

        table_result = json.loads(table_output.read_text(encoding="utf-8"))

        # Logo recognition
        logo_input = tmpdir / "logo_input.json"
        logo_output = tmpdir / "logo_output.json"
        logo_input.write_text(json.dumps({
            "document_id": table_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": table_result["source_uri"],
            "pages": table_result["pages"]
        }), encoding="utf-8")

        with patch.dict(os.environ, {"LOGO_INPUT": str(logo_input), "LOGO_OUTPUT": str(logo_output)}):
            logo_mod.main()

        logo_result = json.loads(logo_output.read_text(encoding="utf-8"))

        # Fraud detection
        fraud_input = tmpdir / "fraud_input.json"
        fraud_output = tmpdir / "fraud_output.json"
        fraud_input.write_text(json.dumps({
            "document_id": logo_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": logo_result["source_uri"],
            "pages": logo_result["pages"]
        }), encoding="utf-8")

        with patch.dict(os.environ, {"FRAUD_INPUT": str(fraud_input), "FRAUD_OUTPUT": str(fraud_output)}):
            fraud_mod.main()

        fraud_result = json.loads(fraud_output.read_text(encoding="utf-8"))

        # Aggregation
        agg_input = tmpdir / "aggregation_input.json"
        agg_output = tmpdir / "aggregation_output.json"
        agg_input.write_text(json.dumps({
            "document_id": fraud_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": fraud_result["source_uri"],
            "pages": fraud_result["pages"]
        }), encoding="utf-8")

        with patch.dict(os.environ, {"AGGREGATION_INPUT": str(agg_input), "AGGREGATION_OUTPUT": str(agg_output)}):
            aggregation_mod.main()

        aggregation_result = json.loads(agg_output.read_text(encoding="utf-8"))

        print(json.dumps({
            "manifest_status": manifest_result["persistence"]["status"],
            "page_count": aggregation_result["canonical_document"]["metadata"]["page_count"],
            "tables_detected": aggregation_result["canonical_document"]["metadata"]["tables_detected"],
            "logos_detected": aggregation_result["canonical_document"]["metadata"]["logos_detected"],
            "fraud_flags_detected": aggregation_result["canonical_document"]["metadata"]["fraud_flags_detected"]
        }, indent=2))


if __name__ == "__main__":
    main()
