![Phase 3 Pipeline Workflow](phase3_pipeline_workflow.png)

**Figure:** Full Phase 3 pipeline workflow. Image stored in S3 at:
`s3://ocr-rebuild-program/docs/01_architecture/phase3_pipeline_workflow.png`

# Aggregation Pipeline Design

## Description
Combines outputs from Preprocessing, OCR, Table Extraction, Logo/Template Recognition, and Fraud Detection pipelines into a unified canonical document structure for downstream processing, reporting, and client consumption.

## Inputs / Outputs
- **Inputs:** 
  - Preprocessed documents (`preprocessing_pipeline.md`)
  - OCR results (`ocr_pipeline.md`)
  - Table extraction results (`table_extraction_pipeline.md`)
  - Logo/Template recognition metadata (`logo_template_pipeline.md`)
  - Fraud detection results (`fraud_detection_pipeline.md`)
- **Outputs:** 
  - Fully aggregated canonical document objects
  - Includes structured tables, text blocks, metadata, template/logo annotations, and fraud flags
  - Conforms to `canonical_document_schema.json`

## Processing Steps
1. Validate inputs from all upstream pipelines
2. Merge page-level OCR text with table structures
3. Integrate template/logo recognition metadata
4. Attach fraud/anomaly flags
5. Consolidate metadata (page count, processing times, engine info)
6. Perform consistency checks across all fields
7. Generate final canonical JSON document per input

## Conditional Logic / Routing
- Skip aggregation if document already aggregated successfully
- Partial aggregation supported for documents with only subset of pipeline outputs
- Route incomplete aggregation for reprocessing if upstream failures detected

## Error Handling & Client Guidance
- Retry aggregation on transient failures
- Log and notify client on aggregation errors
- Provide error codes for integration
- Flag documents requiring manual review due to missing data

## Performance Placeholders
- Estimated throughput: X documents/sec
- Estimated batch latency: Y minutes per 100-page document
- Resource usage per aggregation process

## Modularity / Future Extensions
- Support plugin-based post-processing modules (format conversions, indexing)
- Enable aggregation of additional pipelines (e.g., advanced analytics)
- Extend for multi-document packages (bundled submissions)
- Allow output in multiple formats (JSON, XML, PDF summary)

## References
- Preprocessing pipeline: `preprocessing_pipeline.md`
- OCR pipeline: `ocr_pipeline.md`
- Table extraction pipeline: `table_extraction_pipeline.md`
- Logo/Template pipeline: `logo_template_pipeline.md`
- Fraud detection pipeline: `fraud_detection_pipeline.md`
- Canonical schema: `canonical_document_schema.json`
- Evaluation framework: `evaluation_framework.md`
