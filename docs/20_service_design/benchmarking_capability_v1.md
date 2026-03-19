# Benchmarking Capability v1

## Purpose
Provide population-level and category-level benchmarking for financial metrics to contextualize individual customer behaviour, affordability, and spending patterns.

---

## Inputs

Field | Description | Source
------|-------------|--------
behavioural_metrics | Metrics from behavioural analysis | Behavioural Analysis Capability
cash_flow_summary | Aggregated cash flow per period | Cash Flow Classification
category_spend_summary | Category-level spend totals | Category Classification
pricing_data | Relevant product, insurance, or loan pricing | External or internal APIs
population_data | Aggregated benchmark data | Historical anonymised dataset

---

## Processing Logic

- Compare individual metrics to population percentiles
- Calculate ratios against category-specific benchmarks
- Determine over/under-spending relative to peer group
- Evaluate affordability or financial stress relative to benchmarks
- Optionally adjust benchmarks for temporal trends, geography, or account type

---

## Outputs

Example output structure:

{
  "benchmarking_results": [
    {
      "metric_name": "groceries_spend_percentile",
      "value": 85,
      "confidence": 0.90
    },
    {
      "metric_name": "transport_spend_percentile",
      "value": 60,
      "confidence": 0.92
    }
  ],
  "metadata": {
    "benchmark_population": "regional",
    "period_start": "YYYY-MM-DD",
    "period_end": "YYYY-MM-DD",
    "transactions_analyzed": 120
  }
}

---

## Failure Modes

- Incomplete population data
- Mismatch between customer profile and benchmark cohort
- Outdated or stale historical data
- Missing category spend summaries

---

## Dependencies

- Behavioural analysis metrics
- Cash flow classification
- Category classification
- Historical benchmark datasets

---

## Cost Consideration

- Medium compute if performing large-scale comparisons
- Data storage for historical benchmarks
- Optional API costs if using external data sources

---

## Why this capability is critical

- Provides context for customer financial behaviour
- Supports affordability and risk assessment
- Enables differentiation via benchmarking insights
- Foundations for advanced advisory and optimisation services
