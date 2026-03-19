# Benchmarking — Capability v1

## Purpose
Compare client data against population, pricing, and category benchmarks.

## Inputs
- cash_flow_classification
- transaction categories
- debt positions

## Processing Logic
- Calculate averages per category
- Compare client spending vs peers
- Identify over/under-spending
- Price benchmarking vs industry standards

## Outputs
{
  "benchmark_scores": [
    {
      "category": "transport",
      "client_value": 200.00,
      "peer_average": 150.00,
      "benchmark_flag": "high|low|normal",
      "confidence": 0.92
    }
  ]
}

## Failure Modes
- Missing category data
- Insufficient population comparison data
- Inaccurate prior classification

## Dependencies
- Category classification
- Cash flow classification
- Debt detection

## Cost Consideration
- Low to medium compute
- May require external datasets

## Why this capability is critical
Enables pricing insights, spending comparisons, and trend benchmarks.
