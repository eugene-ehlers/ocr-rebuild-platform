import importlib.util
import json
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


def load_json(relative_path: str):
    with open(REPO_ROOT / relative_path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_test_image_bytes():
    img = Image.new("RGB", (20, 20), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_document_manifest_schema_is_valid_json():
    data = load_json("docs/03_data_model/document_manifest_schema.json")
    assert data["title"] == "document_manifest_schema"


def test_page_schema_is_valid_json():
    data = load_json("docs/03_data_model/page_schema.json")
    assert data["title"] == "page_schema"


def test_canonical_document_schema_is_valid_json():
    data = load_json("docs/03_data_model/canonical_document_schema.json")
    assert data["title"] == "canonical_document_schema"


def test_ocr_output_schema_is_valid_json():
    data = load_json("docs/03_data_model/ocr_output_schema.json")
    assert data["title"] == "ocr_output_schema"


def test_logo_detection_schema_is_valid_json():
    data = load_json("docs/03_data_model/logo_detection_schema.json")
    assert data["title"] == "logo_detection_schema"


def test_fraud_findings_schema_is_valid_json():
    data = load_json("docs/03_data_model/fraud_findings_schema.json")
    assert data["title"] == "fraud_findings_schema"


def test_entity_extraction_schema_is_valid_json():
    data = load_json("docs/03_data_model/entity_extraction_schema.json")
    assert data["title"] == "entity_extraction_schema"


def test_manifest_generator_contract():
    mod = load_module("manifest_generator", "services/manifest_generator/lambda_function.py")

    with patch.object(mod, "save_manifest", return_value={"status": "saved", "manifest_id": "UNKNOWN"}):
        result = mod.lambda_handler({"document_id": "doc-1", "source_uri": "s3://bucket/file.pdf"}, None)

    assert result["statusCode"] == 200
    assert "manifest" in result
    assert "persistence" in result
    manifest = result["manifest"]
    assert manifest["manifest_id"] == "UNKNOWN"
    assert manifest["documents"][0]["document_id"] == "doc-1"
    assert "pipeline_history" in manifest
    assert result["persistence"]["status"] == "saved"


def test_preprocessing_contract():
    mod = load_module("preprocessing", "services/preprocessing/lambda_function.py")

    test_bytes = make_test_image_bytes()

    class MockBody:
        def read(self):
            return test_bytes

    class MockS3:
        def get_object(self, Bucket, Key):
            return {"Body": MockBody()}

        def put_object(self, Bucket, Key, Body, ContentType):
            assert Bucket is not None
            assert Key.endswith(".png") or "processed/" in Key
            assert ContentType == "image/png"
            assert isinstance(Body, (bytes, bytearray))

    with patch.object(mod, "s3", MockS3()):
        result = mod.lambda_handler(
            {
                "document_id": "doc-1",
                "source_uri": "s3://bucket/file.pdf",
                "source_bucket": "source-bucket",
                "pages": [{"page_number": 1, "s3_key": "uploads/page1.png"}]
            },
            None
        )

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "manifest_update" in result
    assert result["pages"][0]["preprocessing_params"]["status"] == "completed_real_increment"


def test_ocr_contract():
    mod = load_module("ocr_worker", "services/ocr/ocr_worker.py")

    test_bytes = make_test_image_bytes()

    class MockBody:
        def read(self):
            return test_bytes

    class MockS3:
        def get_object(self, Bucket, Key):
            return {"Body": MockBody()}

    with patch.object(mod, "s3", MockS3()):
        with patch.object(mod.pytesseract, "image_to_string", return_value="hello world"):
            result = mod.run(
                {
                    "document_id": "doc-1",
                    "source_uri": "s3://bucket/file.pdf",
                    "pages": [{"page_number": 1, "processed_key": "processed/page1.png"}]
                }
            )

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result
    assert result["pages"][0]["extracted_text"] == "hello world"
    assert result["pages"][0]["engine_name"] == "tesseract"


def test_table_extraction_contract():
    mod = load_module("table_worker", "services/table_extraction/table_worker.py")
    result = mod.build_output(
        {
            "document_id": "doc-1",
            "manifest_id": "man-1",
            "source_uri": "s3://bucket/file.pdf",
            "pages": [
                {
                    "page_number": 1,
                    "extracted_text": "name | age\njohn | 30\nmary | 25"
                }
            ]
        }
    )

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result
    assert len(result["pages"][0]["tables"]) == 1
    assert result["pages"][0]["tables"][0]["table_name"] == "heuristic_text_table"
    assert result["metadata"]["tables_detected"] == 1


def test_logo_recognition_contract():
    mod = load_module("logo_worker", "services/logo_recognition/logo_worker.py")
    result = mod.build_output(
        {
            "document_id": "doc-1",
            "manifest_id": "man-1",
            "source_uri": "s3://bucket/file.pdf",
            "pages": [
                {
                    "page_number": 1,
                    "extracted_text": "Tax Invoice\nInvoice Number: 12345"
                }
            ]
        }
    )

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result
    assert len(result["pages"][0]["metadata"]["logos"]) >= 1
    assert result["pages"][0]["metadata"]["logos"][0]["label"] == "invoice"
    assert result["metadata"]["logos_detected"] >= 1


def test_fraud_detection_contract():
    mod = load_module("fraud_worker", "services/fraud_detection/fraud_worker.py")
    result = mod.build_output(
        {
            "document_id": "doc-1",
            "manifest_id": "man-1",
            "source_uri": "s3://bucket/file.pdf",
            "pages": [
                {"page_number": 1, "extracted_text": ""},
                {"page_number": 2, "extracted_text": "same text on page"},
                {"page_number": 3, "extracted_text": "same text on page"}
            ]
        }
    )

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result
    assert len(result["pages"][0]["metadata"]["fraud_flags"]) >= 1
    assert result["pages"][0]["metadata"]["fraud_flags"][0]["flag_type"] == "blank_page_text"
    duplicate_flags = result["pages"][2]["metadata"]["fraud_flags"]
    assert any(flag["flag_type"] == "duplicate_page_text" for flag in duplicate_flags)
    assert result["metadata"]["fraud_flags_detected"] >= 2


def test_aggregation_contract():
    mod = load_module("aggregation_worker", "services/aggregation/aggregation_worker.py")
    result = mod.build_output({"document_id": "doc-1", "manifest_id": "man-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert "canonical_document" in result
    assert "manifest_update" in result
    assert result["canonical_document"]["document_id"] == "doc-1"
