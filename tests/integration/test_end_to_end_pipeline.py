import importlib.util
import io
from pathlib import Path
from unittest.mock import patch

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[2]


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


def test_end_to_end_pipeline_flow():
    manifest_mod = load_module("manifest_generator", "services/manifest_generator/lambda_function.py")
    preprocessing_mod = load_module("preprocessing", "services/preprocessing/lambda_function.py")
    ocr_mod = load_module("ocr_worker", "services/ocr/ocr_worker.py")
    table_mod = load_module("table_worker", "services/table_extraction/table_worker.py")
    logo_mod = load_module("logo_worker", "services/logo_recognition/logo_worker.py")
    fraud_mod = load_module("fraud_worker", "services/fraud_detection/fraud_worker.py")
    aggregation_mod = load_module("aggregation_worker", "services/aggregation/aggregation_worker.py")

    # 1. Manifest generation
    with patch.object(manifest_mod, "save_manifest", return_value={"status": "saved", "manifest_id": "UNKNOWN"}):
        manifest_result = manifest_mod.lambda_handler(
            {
                "document_id": "doc-1",
                "source_uri": "s3://bucket/file.pdf",
                "pages": [{"page_number": 1, "s3_key": "uploads/page1.png"}]
            },
            None
        )

    assert manifest_result["statusCode"] == 200
    assert "manifest" in manifest_result

    # 2. Preprocessing
    test_bytes = make_test_image_bytes()

    class MockBody:
        def read(self):
            return test_bytes

    class MockPreprocessS3:
        def get_object(self, Bucket, Key):
            return {"Body": MockBody()}

        def put_object(self, Bucket, Key, Body, ContentType):
            assert ContentType == "image/png"

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

    assert len(preprocessing_result["pages"]) == 1

    # 3. OCR
    class MockOcrS3:
        def get_object(self, Bucket, Key):
            return {"Body": MockBody()}

    with patch.object(ocr_mod, "s3", MockOcrS3()):
        with patch.object(
            ocr_mod.pytesseract,
            "image_to_string",
            return_value="Tax Invoice\nInvoice Number: 12345\nname | age\njohn | 30\nmary | 25"
        ):
            ocr_result = ocr_mod.run(preprocessing_result)

    assert len(ocr_result["pages"]) == 1
    assert "Tax Invoice" in ocr_result["pages"][0]["extracted_text"]

    # 4. Table extraction
    table_result = table_mod.build_output(
        {
            "document_id": ocr_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": ocr_result["source_uri"],
            "pages": ocr_result["pages"]
        }
    )

    assert len(table_result["pages"][0]["tables"]) == 1

    # 5. Logo recognition
    logo_result = logo_mod.build_output(
        {
            "document_id": table_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": table_result["source_uri"],
            "pages": table_result["pages"]
        }
    )

    assert len(logo_result["pages"][0]["metadata"]["logos"]) >= 1

    # 6. Fraud detection
    fraud_result = fraud_mod.build_output(
        {
            "document_id": logo_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": logo_result["source_uri"],
            "pages": logo_result["pages"]
        }
    )

    assert "fraud_flags" in fraud_result["pages"][0]["metadata"]

    # 7. Aggregation
    aggregation_result = aggregation_mod.build_output(
        {
            "document_id": fraud_result["document_id"],
            "manifest_id": "man-1",
            "source_uri": fraud_result["source_uri"],
            "pages": fraud_result["pages"]
        }
    )

    canonical = aggregation_result["canonical_document"]
    summary = canonical["metadata"]

    assert canonical["document_id"] == "doc-1"
    assert summary["page_count"] == 1
    assert summary["tables_detected"] == 1
    assert summary["logos_detected"] >= 1
    assert summary["total_extracted_characters"] > 0
