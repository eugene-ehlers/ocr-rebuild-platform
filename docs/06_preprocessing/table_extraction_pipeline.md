![Phase 3 Pipeline Workflow](phase3_pipeline_workflow.png)

**Figure:** Full Phase 3 pipeline workflow. Image stored in S3 at:
`s3://ocr-rebuild-program/docs/01_architecture/phase3_pipeline_workflow.png`

# Table Extraction Pipeline Design

## Description
Extracts structured tables from OCR text and document images, preserving positional relationships and formatting for downstream data processing.

## Inputs / Outputs
- **Inputs:** OCR results (`ocr_pipeline.md` output), preprocessed document images
- **Outputs:** Structured table objects in canonical JSON format (`canonical_document_schema.json`) with row/column coordinates and cell content

## Processing Steps
1. Identify table regions using positional metadata and template recognition hints
2. Detect rows, columns, and merged cells
3. Extract text from each cell, associating with positional coordinates
4. Preserve table formatting (borders, spans) where available
5. Annotate confidence per cell and per table
6. Aggregate all tables per document
7. Integrate with canonical document schema

## Conditional Logic / Routing
- Skip table extraction if no tables detected
- Route complex tables (>50 cells) to parallel extraction
- Conditional fallback to alternative extraction algorithms for low-confidence tables

## Error Handling & Client Guidance
- Retry extraction for failed tables up to 2 times
- Log and notify client of extraction failures
- Provide error codes for integration
- Mark low-confidence tables for manual review

## Performance Placeholders
- Estimated throughput: X tables/sec (small docs)
- Estimated batch latency: Y minutes for 100-page document
- Resource usage per extraction algorithm

## Modularity / Future Extensions
- Plugin-based table detection/extraction algorithms
- Support multi-page table spanning
- Extend for embedded images within tables
- Enable export to multiple formats (CSV, JSON, Excel)

## References
- OCR pipeline: `ocr_pipeline.md`
- Canonical schema: `canonical_document_schema.json`
- Evaluation framework: `evaluation_framework.md`
