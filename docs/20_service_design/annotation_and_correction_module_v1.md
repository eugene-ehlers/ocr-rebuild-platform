# Annotation and Correction Module v1

## 1. Purpose

Allows users to:
- add context to OCR results
- correct interpretations
- support reprocessing
- contribute to future model training

---

## 2. Core Principle

Original OCR data must NEVER be overwritten.

---

## 3. Capabilities

- add annotation
- edit annotation
- view annotation history
- submit for review
- trigger reprocessing

---

## 4. Data Model (Conceptual)

- annotation_id
- document_id
- field_reference
- original_value
- system_interpretation
- user_suggestion
- reviewer_status
- final_value

---

## 5. Workflow

1. OCR extracts data
2. system interprets data
3. user adds correction/comment
4. system stores annotation
5. reviewer (future) validates
6. system optionally reprocesses

---

## 6. Use Cases

- ATM withdrawal classified as fuel
- unclear merchant reclassified
- income categorisation correction

---

## 7. Integration

- document workspace
- request/results module
- ML training pipeline (future)

