import importlib.util
import json
from pathlib import Path


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
    result = mod.lambda_handler({"document_id": "doc-1", "source_uri": "s3://bucket/file.pdf"}, None)

    assert result["statusCode"] == 200
    assert "manifest" in result
    manifest = result["manifest"]
    assert manifest["manifest_id"] == "UNKNOWN"
    assert manifest["documents"][0]["document_id"] == "doc-1"
    assert "pipeline_history" in manifest


def test_preprocessing_contract():
    mod = load_module("preprocessing", "services/preprocessing/lambda_function.py")
    result = mod.lambda_handler({"document_id": "doc-1", "source_uri": "s3://bucket/file.pdf", "pages": []}, None)

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "manifest_update" in result


def test_ocr_contract():
    mod = load_module("ocr_worker", "services/ocr/ocr_worker.py")
    result = mod.run({"document_id": "doc-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result


def test_table_extraction_contract():
    mod = load_module("table_worker", "services/table_extraction/table_worker.py")
    result = mod.build_output({"document_id": "doc-1", "manifest_id": "man-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result


def test_logo_recognition_contract():
    mod = load_module("logo_worker", "services/logo_recognition/logo_worker.py")
    result = mod.build_output({"document_id": "doc-1", "manifest_id": "man-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result


def test_fraud_detection_contract():
    mod = load_module("fraud_worker", "services/fraud_detection/fraud_worker.py")
    result = mod.build_output({"document_id": "doc-1", "manifest_id": "man-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert result["document_id"] == "doc-1"
    assert "pages" in result
    assert "metadata" in result
    assert "manifest_update" in result


def test_aggregation_contract():
    mod = load_module("aggregation_worker", "services/aggregation/aggregation_worker.py")
    result = mod.build_output({"document_id": "doc-1", "manifest_id": "man-1", "source_uri": "s3://bucket/file.pdf", "pages": []})

    assert "canonical_document" in result
    assert "manifest_update" in result
    assert result["canonical_document"]["document_id"] == "doc-1"
