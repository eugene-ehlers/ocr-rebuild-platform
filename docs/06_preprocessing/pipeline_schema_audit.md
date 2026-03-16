![Phase 3 Pipeline Workflow](phase3_pipeline_workflow.png)

**Figure:** Full Phase 3 pipeline workflow. Image stored in S3 at:
`s3://ocr-rebuild-program/docs/01_architecture/phase3_pipeline_workflow.png`

# OCR Pipeline Schema Audit – Phase 3

## Canonical Document Schema – Enhanced Fields

| Field Name | Required? | Nested? | Source/Pipeline | Notes / Phase 2 Additions |
|------------|-----------|---------|----------------|---------------------------|
| document_id | Yes | No | All pipelines | Unique document identifier |
| source_uri | No | No | Ingestion | Original document location |
| document_type | No | No | Classification | Default UNKNOWN |
| ingestion_timestamp | No | No | Ingestion | ISO 8601 |
| pages | No | Yes | OCR / Preprocessing | Array of page objects |
| pages.page_number | Yes | No | OCR | Sequential page number |
| pages.extracted_text | No | No | OCR | Default UNKNOWN; contains all text on page |
| pages.rotation_angle | No | No | Preprocessing | Detected rotation for correction |
| pages.orientation | No | No | Preprocessing | Page orientation detection |
| pages.language_code | No | No | OCR | Language code per page; supports multi-language pages |
| pages.preprocessing_params | No | Yes | Preprocessing | Parameters of contrast, skew, enhancement, etc. |
| pages.line_block_word_confidence | No | Yes | OCR | Granular confidence scores per line/block/word |
| pages.tables | No | Yes | Table Extraction | Array of table objects |
| pages.tables.table_id | Yes | No | Table Extraction | Unique table identifier per page |
| pages.tables.table_name | No | No | Table Extraction | Optional table label |
| pages.tables.page_number | Yes | No | Table Extraction | Page reference |
| pages.tables.rows | Yes | Yes | Table Extraction | Array of row objects |
| pages.tables.rows.row_index | Yes | No | Table Extraction | Row position |
| pages.tables.rows.cells | Yes | Yes | Table Extraction | Array of cell objects |
| pages.tables.rows.cells.column_name | Yes | No | Table Extraction | Column identifier |
| pages.tables.rows.cells.cell_text | Yes | No | Table Extraction | Extracted cell text |
| pages.tables.rows.cells.confidence_score | No | No | Table Extraction | OCR confidence per cell |
| pages.metadata | No | Yes | All pipelines | Phase 2: engine metadata, preprocessing results, fraud flags, pipeline_history, etc. |
| pages.previous_version_id | No | No | All pipelines | For document lineage and reprocessing trace |
| pages.multi_layer_text | No | Yes | OCR | Optional text layers for multi-language or multi-engine outputs |
| pages.engine_name | No | No | OCR / Table Extraction | Engine used for this page |
| pages.engine_version | No | No | OCR / Table Extraction | Engine version for traceability |

## Document Manifest Schema – Enhanced Fields

| Field Name | Required? | Nested? | Pipeline Action | Notes / Phase 2 Additions |
|------------|-----------|---------|----------------|---------------------------|
| manifest_id | Yes | No | All pipelines | Unique manifest identifier |
| creation_timestamp | No | No | Ingestion | ISO 8601 |
| source_batch_uri | No | No | Batch ingest | Original batch location |
| documents | No | Yes | All pipelines | Array of document entries |
| documents.document_id | Yes | No | All pipelines | Reference to canonical document_id |
| documents.source_uri | No | No | All pipelines | Optional duplicate |
| documents.expected_document_type | No | No | Classification | Default UNKNOWN |
| processing_parameters | No | Yes | Batch | Config used for batch |
| pipeline_status | No | No | All pipelines | completed/failed/partial |
| retry_count | No | No | All pipelines | Incremented per failed page/batch |
| last_updated | No | No | All pipelines | ISO timestamp |
| partial_execution_flags | No | No | All pipelines | Per-page or per-step indicator |
| client_notification | No | No | All pipelines | If client should be notified |
| pipeline_history | No | Yes | All pipelines | Tracks previous versions, processing steps, engine used, timestamps |

## Pipeline Audit – 06_preprocessing (Enhanced)

### Canonical Fields

| Field Name | Required? | Source/Pipeline | Currently Implemented | Notes / Phase 2 Missing |
|------------|-----------|----------------|--------------------|-------------------------|
| document_id | Yes | All pipelines | ✅ | — |
| source_uri | No | Ingestion | ✅ | — |
| document_type | No | Classification | ❌ | Phase 2 placeholder |
| ingestion_timestamp | No | Ingestion | ✅ | — |
| pages | No | OCR / Preprocessing | ✅ | — |
| pages.page_number | Yes | OCR | ✅ | — |
| pages.extracted_text | No | OCR | ✅ | — |
| pages.rotation_angle | No | Preprocessing | ❌ | Phase 2 placeholder |
| pages.orientation | No | Preprocessing | ❌ | Phase 2 placeholder |
| pages.language_code | No | OCR | ❌ | Phase 2 placeholder |
| pages.preprocessing_params | No | Preprocessing | ❌ | Phase 2 placeholder |
| pages.line_block_word_confidence | No | OCR | ❌ | Phase 2 placeholder |
| pages.tables | No | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.table_id | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.table_name | No | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.page_number | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows.row_index | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows.cells | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows.cells.column_name | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows.cells.cell_text | Yes | Table Extraction | ❌ | Phase 2 placeholder |
| pages.tables.rows.cells.confidence_score | No | Table Extraction | ❌ | Phase 2 placeholder |
| pages.metadata | No | All pipelines | ❌ | Phase 2 placeholder |
| pages.previous_version_id | No | All pipelines | ❌ | Phase 2 placeholder |
| pages.multi_layer_text | No | OCR | ❌ | Phase 2 placeholder |
| pages.engine_name | No | OCR / Table Extraction | ❌ | Phase 2 placeholder |
| pages.engine_version | No | OCR / Table Extraction | ❌ | Phase 2 placeholder |

### Manifest Fields

| Field Name | Pipeline Action | Currently Implemented | Notes / Phase 2 Missing |
|------------|----------------|--------------------|-------------------------|
| manifest_id | All pipelines | ✅ | — |
| creation_timestamp | Ingestion | ✅ | — |
| source_batch_uri | Batch ingest | ✅ | — |
| documents.document_id | All pipelines | ✅ | — |
| documents.source_uri | All pipelines | ✅ | — |
| documents.expected_document_type | Classification | ❌ | Phase 2 placeholder |
| processing_parameters | Batch | ✅ | — |
| pipeline_status | Updated per stage | ❌ | Phase 2 placeholder |
| retry_count | Incremented per failure | ❌ | Phase 2 placeholder |
| last_updated | Updated per stage | ✅ | — |
| partial_execution_flags | Set per page/batch | ❌ | Phase 2 placeholder |
| client_notification | Triggered if needed | ❌ | Phase 2 placeholder |
| pipeline_history | Tracked per document | ❌ | Phase 2 placeholder |

