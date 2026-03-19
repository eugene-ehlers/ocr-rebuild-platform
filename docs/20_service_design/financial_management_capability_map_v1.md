# Financial Management — Capability Map v1

## Purpose

This document defines the **technical capability layer** required to deliver the Financial Management service menu.

It sits between:
- Service design (what we promise)
- Decision engine (what to call when)
- OCR payload design (what data must exist)

---

## Capability Categories

### 1. OCR & Extraction (Foundation)

| Capability | Source | Build vs Buy | Notes |
|----------|--------|-------------|------|
| OCR text extraction | Textract / Google / Azure | Buy | Multi-engine routing |
| Table extraction | OCR engine / custom | Hybrid | Required for transactions |
| Layout understanding | OCR engine | Buy | Needed for structure |

---

### 2. Normalisation & Structuring

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Transaction parsing | Build | Critical IP |
| Date normalisation | Build | Multi-format |
| Amount normalisation | Build | Currency handling |
| Account identification | Build | Multi-account docs |

---

### 3. Classification Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Transaction category classification | Build/Model | Groceries, transport, etc |
| Cash flow classification | Build/Model | Income vs expense |
| Debt detection classification | Build/Model | Loans, repayments |
| Behavioural classification | Build/Model | Spending patterns |

NOTE: Multiple classifiers required — not one model.

---

### 4. Enrichment Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Merchant enrichment | External API | Optional |
| Category mapping refinement | Build | Improves accuracy |
| Geo / channel inference | Build | POS vs EFT |

---

### 5. Analytics Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Cash flow calculation | Build | Core |
| Trend analysis | Build | Multi-period |
| Frequency analysis | Build | Behaviour detection |
| Outlier detection | Model | Alerts |

---

### 6. Benchmarking Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Population benchmarks | Build (later) | Requires data scale |
| Pricing comparison | External + Build | Insurance, loans |
| Category spend comparison | Build | Core differentiator |

---

### 7. Explanation Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Statement summarisation | Model + rules | Customer-facing |
| Plain language explanation | Model | Key differentiator |
| Internal trace explanation | Build | Debug + audit |

---

### 8. Optimisation & Advice Layer

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Spend optimisation suggestions | Model + rules | Reduce cost |
| Timing optimisation | Build | Payment timing |
| Debt improvement insights | Model | High value |

---

### 9. Risk & Stress Detection

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Financial stress detection | Model | Core |
| Liquidity risk scoring | Model | Core |
| Over-indebtedness detection | Model | Lending crossover |

---

### 10. Document & Proof Services

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Payment proof generation | Build | Differentiator |
| Document authenticity validation | Build | Critical |
| Audit trace generation | Build | Compliance |

---

### 11. Language & Translation (Optional but Required for Scale)

| Capability | Build vs Buy | Notes |
|----------|-------------|------|
| Language detection | Model | Required |
| Translation | API | Multi-language support |

---

## Key Design Principles

- Multiple models per function (NOT single classifier)
- Decision engine chooses capability at runtime
- OCR is ONLY a supplier, not the system
- All capabilities must declare:
  - input schema
  - output schema
  - confidence
  - cost


---

# Detailed Capability Specification

## Capability: Transaction Parsing

### Purpose

Convert raw OCR and extracted table output into structured financial transactions.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| raw_text | OCR extracted text | OCR engine |
| tables | Extracted tables | OCR engine |
| document_type | Statement type | Classification |
| layout_metadata | Page structure and layout hints | OCR engine |

### Processing Logic

- Identify transaction table regions
- Extract rows into structured transaction objects
- Detect:
  - transaction date
  - transaction description
  - debit or credit indicator
  - transaction amount
  - running balance where available
- Handle:
  - multi-line descriptions
  - inconsistent row formats
  - missing or ambiguous headers
  - issuer-specific statement layouts

### Outputs

Example output structure:

{
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": -100.00,
      "type": "debit|credit",
      "balance": 1000.00,
      "confidence": 0.95
    }
  ],
  "metadata": {
    "total_transactions": 120,
    "parsing_confidence": 0.92
  }
}

### Failure Modes

- Table not detected
- Misaligned columns
- OCR errors in amount fields
- Missing dates
- Description split across rows
- Opening or closing balance confused as transaction rows

### Dependencies

- OCR output quality
- Table extraction accuracy
- Issuer or layout recognition where available

### Cost Consideration

- Low compute
- Rule-based and parsing heavy
- No external API required in baseline design

### Why this capability is critical

This capability is foundational to:
- transaction classification
- cash flow analysis
- spending analysis
- indebtedness analysis
- benchmarking
- explanation services

If transaction parsing is unreliable, downstream financial management outputs become unreliable.


---

## Capability: Transaction Category Classification

### Purpose

Assign each parsed transaction to one or more semantic financial categories so downstream services can analyse spending, income, indebtedness, pricing, behaviour, and trends.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transaction_date | Normalised transaction date | Transaction parsing |
| transaction_description | Parsed transaction narration | Transaction parsing |
| transaction_amount | Normalised signed amount | Transaction parsing |
| transaction_type | Debit or credit indicator | Transaction parsing |
| running_balance | Running balance where available | Transaction parsing |
| issuer_context | Bank, template, or institution context | Classification / issuer recognition |
| language_code | Language of source text | Language detection |
| merchant_name | Normalised merchant where available | Merchant enrichment |

### Processing Logic

- Classify each transaction into semantic categories such as:
  - salary or income
  - groceries
  - transport
  - utilities
  - rent
  - loan repayment
  - insurance
  - transfers
  - fees and charges
  - cash withdrawal
  - entertainment
  - medical
  - education
  - savings or investment
- Support:
  - primary category
  - optional secondary category
  - confidence per classification
- Allow:
  - issuer-specific rules
  - language-aware rules
  - merchant-aware overrides
  - rule-first baseline with model refinement where needed

### Outputs

Example output structure:

{
  "classified_transactions": [
    {
      "transaction_id": "string",
      "primary_category": "transport",
      "secondary_category": "fuel",
      "classification_confidence": 0.93,
      "classification_method": "rules|model|hybrid"
    }
  ],
  "metadata": {
    "total_classified": 120,
    "classification_confidence_overall": 0.89
  }
}

### Failure Modes

- Description too vague to classify
- Merchant not recognised
- Language ambiguity
- Category collision across multiple possible meanings
- OCR narration quality too poor for reliable classification

### Dependencies

- Transaction parsing
- Merchant enrichment where available
- Language detection where needed
- Issuer recognition where helpful

### Cost Consideration

- Low to medium in baseline rules-first design
- Higher if model-based enrichment is invoked
- External merchant enrichment may add API cost

### Why this capability is critical

This capability is foundational to:
- spending analysis
- income analysis
- indebtedness analysis
- pricing and benchmarking
- behaviour insights
- trend analysis

A single classifier is not sufficient for the full platform, but semantic transaction category classification is the first classification layer that many downstream services depend on.


---

## Capability: Cash Flow Classification

### Purpose

Classify transactions into financial flow types that describe how money moves through the account, enabling affordability, financial health, and risk analysis.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transaction_amount | Signed transaction amount | Transaction parsing |
| transaction_type | Debit or credit | Transaction parsing |
| primary_category | Category classification | Category classification |
| secondary_category | Optional sub-category | Category classification |
| transaction_description | Raw narration | Transaction parsing |
| historical_transactions | Prior period transactions | Data store |
| account_context | Account type and profile | Metadata |

### Processing Logic

- Classify transactions into financial flow types such as:
  - income (salary, transfers in)
  - fixed expenses (rent, insurance, loan repayments)
  - variable essential expenses (groceries, utilities)
  - discretionary expenses (entertainment, dining)
  - debt-related flows (repayments, new credit)
  - savings and investments
- Determine:
  - recurring vs non-recurring flows
  - fixed vs variable nature
- Use:
  - rules based on category + patterns
  - temporal analysis for recurrence
  - optional model refinement

### Outputs

Example output structure:

{
  "cash_flow_classification": [
    {
      "transaction_id": "string",
      "flow_type": "fixed_expense",
      "sub_type": "insurance",
      "recurrence": "monthly|irregular",
      "confidence": 0.91
    }
  ],
  "metadata": {
    "income_total": 50000.00,
    "fixed_expense_total": 20000.00,
    "variable_expense_total": 15000.00,
    "discretionary_total": 8000.00
  }
}

### Failure Modes

- Misclassification due to poor category input
- Recurrence detection failure due to limited history
- Ambiguous transactions (e.g. transfers between own accounts)

### Dependencies

- Transaction parsing
- Transaction category classification
- Historical data availability

### Cost Consideration

- Low to medium
- Mostly rule-based with optional model enhancement
- No external API required in baseline

### Why this capability is critical

This capability enables:
- affordability calculations
- financial health scoring
- debt capacity analysis
- optimisation recommendations
- lending integration

It is a core bridge between raw transaction data and financial intelligence.


---

## Capability: Debt / Indebtedness Detection

### Purpose

Identify all debt-related transactions, repayment schedules, and outstanding obligations to enable risk scoring, credit evaluation, and affordability assessment.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transaction_amount | Signed transaction amount | Transaction parsing |
| transaction_type | Debit or credit | Transaction parsing |
| primary_category | Category classification | Category classification |
| secondary_category | Optional sub-category | Category classification |
| cash_flow_type | Cash flow classification | Cash Flow Classification |
| account_context | Account type, profile, and limits | Metadata |
| historical_transactions | Prior debt-related transactions | Data store |

### Processing Logic

- Detect loans, credit facilities, and repayment obligations
- Calculate outstanding balances per facility
- Identify overdue or missed payments
- Track repayment schedules and obligations
- Determine repayment trends (on-time, late, default risk)
- Use rules-based first pass; optional model-based enrichment for complex cases

### Outputs

Example output structure:

{
  "debt_positions": [
    {
      "debt_id": "string",
      "outstanding_balance": 2000.00,
      "monthly_repayment": 500.00,
      "due_date": "YYYY-MM-DD",
      "risk_flag": "low|medium|high",
      "confidence": 0.92
    }
  ],
  "metadata": {
    "total_debt_accounts": 3,
    "total_outstanding_balance": 15000.00,
    "average_risk": "medium"
  }
}

### Failure Modes

- Misidentification of debt vs non-debt transactions
- Missing historical transaction data
- Ambiguous repayment patterns

### Dependencies

- Transaction parsing
- Category classification
- Cash flow classification
- Historical account data

### Cost Consideration

- Medium compute if model-based enrichment used
- Optional external API cost for credit bureau validation

### Why this capability is critical

- Core to credit evaluation, affordability assessment, and financial stress detection
- Provides structured inputs for downstream services in the Financial Management menu


---

## Capability: Benchmarking & Pricing Comparison

### Purpose

Provide comparative insights to customers and internal users, enabling pricing awareness, benchmarking, and financial health evaluation.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transaction_amount | Signed transaction amount | Transaction parsing |
| primary_category | Category classification | Classification Layer |
| cash_flow_type | Cash flow classification | Cash Flow Classification |
| debt_positions | Debt / indebtedness data | Debt Detection Layer |
| account_context | Account type, profile, limits | Metadata |
| historical_transactions | Prior period data | Data store |

### Processing Logic

- Calculate category-wise totals and averages
- Compare client spending vs peer benchmarks
- Compare loan and insurance costs vs market
- Flag unusual spending, high-cost categories
- Optional enrichment using external APIs for insurance / loan rates
- Provide scoring for affordability or pricing awareness

### Outputs

Example output structure:

{
  "benchmarks": [
    {
      "category": "transport",
      "client_total": 1200.00,
      "peer_average": 950.00,
      "deviation_flag": "above_average",
      "confidence": 0.91
    }
  ],
  "pricing_comparisons": [
    {
      "product": "short_term_insurance",
      "client_cost": 500.00,
      "market_average": 450.00,
      "deviation_flag": "above_average",
      "confidence": 0.89
    }
  ],
  "metadata": {
    "total_categories_analyzed": 12,
    "total_products_analyzed": 3
  }
}

### Failure Modes

- Missing historical / benchmark data
- Category misalignment with peer data
- API failures for market data
- Data outliers skewing benchmark comparisons

### Dependencies

- Transaction parsing
- Category classification
- Cash flow classification
- Debt / indebtedness detection
- Historical and peer data store

### Cost Consideration

- Medium compute
- Optional external API costs
- Rule-based scoring for baseline

### Why this capability is critical

- Provides customers insight into spending and cost relative to peers
- Supports internal affordability, lending, and product pricing decisions
- Enhances value of Financial Management service beyond raw statements


---

## Capability: Explanation & Statement Summarisation

### Purpose

Turn processed and classified financial document data into **clear, actionable insights** for customers and internal stakeholders.  
Support both human-friendly summaries and traceable audit information for internal users.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transactions | Structured transaction data | Transaction Parsing Layer |
| transaction_categories | Classified transactions | Category Classification Layer |
| cash_flow_classification | Cash flow data | Cash Flow Classification Layer |
| debt_positions | Outstanding obligations | Debt / Indebtedness Layer |
| benchmarks | Peer and market comparisons | Benchmarking Layer |
| document_metadata | Statement metadata | OCR & Extraction Layer |
| language_code | Language of statement | Language / Translation Layer |

### Processing Logic

- Summarise transactions into:
  - opening & closing balances
  - key inflows and outflows
  - unusual or high-impact transactions
  - category-level spending
  - debt & repayment highlights
- Generate customer-friendly textual explanation
- Produce internal trace log with:
  - reasoning for summaries
  - confidence per section
  - missing or ambiguous data flags
- Support multiple languages if translation layer enabled
- Optional model-based enhancement for natural language explanation

### Outputs

Example output structure:

{
  "summary": {
    "opening_balance": 1200.00,
    "closing_balance": 950.00,
    "inflows": 2000.00,
    "outflows": 2250.00,
    "highlighted_transactions": [
      {"transaction_id":"txn-001","description":"Rent","amount":1000.00,"category":"fixed_expense"}
    ],
    "category_totals": {
      "fixed_expense": 1200.00,
      "variable_expense": 800.00,
      "discretionary": 250.00,
      "savings": 0.00
    },
    "debt_summary": {
      "total_debt": 15000.00,
      "overdue": 500.00,
      "risk_flags": ["medium"]
    },
    "benchmark_summary": {
      "transport": {"client_total":120,"peer_average":100,"flag":"above_average"}
    },
    "plain_language_explanation": "Your balance decreased due to rent and utilities payments; transport spending is above peer average."
  },
  "internal_trace": {
    "section_confidences": {"balances":0.98,"transactions":0.95,"categories":0.93},
    "missing_data_flags": [],
    "document_quality_notes": [],
    "processing_timestamp": "2026-03-19T03:59:20.669665+00:00"
  }
}

### Failure Modes

- Missing or incomplete transaction data
- Misclassified or ambiguous transactions
- OCR errors affecting high-value summaries
- Benchmarking data unavailable
- Translation layer failure for multi-language statements

### Dependencies

- Transaction parsing
- Classification layers
- Cash flow classification
- Debt detection
- Benchmarking
- OCR metadata
- Language / translation if multi-lingual

### Cost Consideration

- Medium compute
- Mostly rule-based, optional model-based text generation
- No external API required for baseline explanations
- Optional translation API cost if multi-language support enabled

### Why this capability is critical

- Provides the **human-facing interpretation** of financial data
- Supports internal **audit, traceability, and compliance**
- Forms the backbone of Financial Management services for decision-making and client communication


---

## Capability: Optimisation & Advice

### Purpose

Provide actionable recommendations to clients based on the processed financial data to **improve financial health, optimise spending, and manage debt effectively**.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| summary | Statement summary with transactions, balances, and category totals | Explanation Layer |
| cash_flow_classification | Classified cash flows | Cash Flow Classification Layer |
| debt_positions | Outstanding debt information | Debt / Indebtedness Layer |
| benchmarks | Peer and market comparison data | Benchmarking Layer |
| historical_trends | Prior period trends and patterns | Data Store |
| document_metadata | Statement metadata | OCR & Extraction Layer |

### Processing Logic

- Analyse cash flow to identify:
  - overspending categories
  - underutilised funds
  - recurring vs irregular expenses
- Analyse debt positions to provide:
  - optimal repayment strategies
  - risk flags for late or missed payments
  - prioritisation of high-interest debts
- Compare client behaviour to benchmarks:
  - highlight above-average spending or underutilisation
  - suggest cost-saving adjustments
- Suggest timing optimisation:
  - best day for payment to avoid overdraft
  - payment schedules to optimise interest savings
- Generate recommendations as:
  - plain-language advice for client
  - structured actionable rules for internal systems

### Outputs

Example output structure:

{
  "recommendations": [
    {
      "recommendation_id": "rec-001",
      "type": "spending_reduction",
      "target_category": "transport",
      "advice_text": "Consider reducing fuel spend by 15% this month",
      "confidence": 0.92
    },
    {
      "recommendation_id": "rec-002",
      "type": "debt_optimisation",
      "target_debt_id": "debt-001",
      "advice_text": "Pay debt-001 one week earlier to reduce interest",
      "confidence": 0.95
    }
  ],
  "metadata": {
    "total_recommendations": 2,
    "overall_confidence": 0.94,
    "processing_timestamp": "2026-03-19T03:59:20.669665+00:00"
  }
}

### Failure Modes

- Missing or incomplete cash flow or debt data
- Ambiguous benchmark comparisons
- Conflict between multiple optimisation goals
- Historical trend data unavailable

### Dependencies

- Explanation / summarisation layer
- Transaction, cash flow, and debt classifications
- Benchmarking layer
- Historical trend data

### Cost Consideration

- Medium compute
- Optional model-based scoring for prioritisation
- No external API required in baseline
- Optional API cost if using advanced benchmarking data

### Why this capability is critical

- Translates raw and classified financial data into actionable recommendations
- Supports **financial wellness, affordability, and planning**
- Provides differentiating value to the client and internal advisory systems


---

## Capability: Risk & Stress Detection

### Purpose

Detect financial stress, liquidity risks, and over-indebtedness to **support credit evaluation, lending decisions, and client advisory services**.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| cash_flow_classification | Classified cash flows | Cash Flow Classification Layer |
| debt_positions | Outstanding debt and repayment schedules | Debt / Indebtedness Layer |
| historical_transactions | Prior periods of transactions | Data Store |
| benchmarks | Population and market benchmarks | Benchmarking Layer |
| document_metadata | Statement metadata | OCR & Extraction Layer |

### Processing Logic

- Analyse cash flow patterns to detect stress indicators:
  - recurring shortfalls
  - negative net balance trends
  - overspending vs income
- Evaluate debt positions:
  - debt-to-income ratios
  - overdue payments
  - repayment burden
- Apply risk scoring models:
  - liquidity risk score
  - over-indebtedness score
  - financial stress level
- Flag accounts for internal advisory attention if thresholds exceeded
- Generate structured outputs for internal dashboards and client-facing advisories

### Outputs

Example output structure:

{
  "risk_scores": [
    {
      "account_id": "acc-001",
      "financial_stress": "medium|high|low",
      "liquidity_risk": 0.72,
      "over_indebtedness": 0.45,
      "confidence": 0.91
    }
  ],
  "metadata": {
    "total_accounts_evaluated": 1,
    "average_confidence": 0.91,
    "processing_timestamp": "2026-03-19T03:59:20.669665+00:00"
  }
}

### Failure Modes

- Missing or incomplete cash flow or debt data
- Inaccurate historical transaction data
- Benchmark comparison not available
- Conflicting input signals

### Dependencies

- Transaction, cash flow, and debt classifications
- Benchmarking layer
- Historical transaction data
- Explanation / summarisation layer

### Cost Consideration

- Medium to high compute if using model-based scoring
- Mostly internal computation; minimal API costs
- Cost scales with number of accounts or documents processed

### Why this capability is critical

- Provides **structured risk insight** for lending, affordability assessment, and client advisory
- Enables proactive detection of financial stress before defaults
- Supports downstream decision-making for optimisation, advice, and monitoring


---

## Capability: Document & Proof Services

### Purpose

Provide verifiable proof of transactions, statements, and financial actions, enabling **compliance, client confidence, and downstream processing**.

### Inputs

| Field | Description | Source |
|------|-------------|--------|
| transactions | Parsed and classified transactions | Transaction Parsing & Classification Layers |
| account_metadata | Account and statement context | Metadata / Data Store |
| document_metadata | Document-level info (dates, balances) | OCR & Extraction Layer |
| risk_scores | Optional stress/risk analysis | Risk & Stress Detection Layer |

### Processing Logic

- Generate **payment proofs** for completed or verified transactions
- Validate **document authenticity** using:
  - OCR and layout metadata
  - Hashing / checksum comparison
  - Known template and logo checks
- Maintain **audit trail** for all documents and operations:
  - timestamps
  - user or system actions
  - versioning and changes
- Format proofs for client or merchant verification
- Ensure outputs meet compliance and internal traceability requirements

### Outputs

Example output structure:

{
  "proofs": [
    {
      "document_id": "doc-001",
      "transaction_id": "txn-001",
      "proof_type": "payment|statement_verification",
      "validity": true,
      "verification_metadata": {
        "hash": "abcd1234",
        "timestamp": "2026-03-19T03:59:20.669665+00:00",
        "engine_used": "OCR Baseline"
      }
    }
  ],
  "audit_trail": [
    {
      "action": "proof_generated",
      "document_id": "doc-001",
      "timestamp": "2026-03-19T03:59:20.669665+00:00",
      "actor": "system"
    }
  ]
}

### Failure Modes

- Missing or invalid input data
- Unrecognised or malformed transaction
- Hash mismatch or document tampering
- Downstream system unable to store or process proof

### Dependencies

- Transaction and category classification
- Risk & Stress Detection
- OCR outputs and document metadata
- Internal audit and storage systems

### Cost Consideration

- Low compute for baseline rules and hashing
- Additional storage cost for audit trail retention
- Optional external verification API costs

### Why this capability is critical

- Provides **trusted financial proofs** for clients, merchants, and internal operations
- Supports compliance, auditing, and regulatory requirements
- Enables secure, traceable documentation for financial actions

