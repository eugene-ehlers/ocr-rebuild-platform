# Financial Management Service Menu — Structured v1

## 1. Service family purpose

Financial Management is the service family that turns financial documents, beginning with statements, into usable financial intelligence for customers and internal users.

It is not OCR as a product.
It is a set of customer-facing and internal-facing services that use OCR, extraction, models, rules, and decision logic to deliver actionable financial outcomes.

## 2. Service family goals

This family must support:

- explanation of what happened in statements
- cash flow understanding
- spending understanding
- indebtedness understanding
- pricing / benchmark awareness
- timing and optimisation insights
- financial stress detection
- trend and health tracking over time
- document-backed proof and authenticity support
- future vault / consent / admin-assistant expansion

## 3. Delivery channels

### Customer-facing
Used by end customers to understand finances, track health, make decisions, and request proof or summaries.

### Internal-facing
Used by internal teams, support, collections, lending, advisors, and operations to inspect confidence, trace decisions, and support customers.

## 4. Service menu structure

Financial Management is structured into Core, Differentiation, and Platform Expansion services.

---

# A. Core Financial Management Services

## A1. Statement Explanation Service

### Customer asks
- What happened in this statement?
- Summarise this statement for me
- Explain my balances, income, and expenses
- Why did my balance change?

### Customer options
- simple summary
- detailed summary
- per statement
- over multiple statements
- customer-friendly explanation
- internal detailed operational explanation

### Customer receives
- opening and closing balance summary
- key inflows and outflows
- major transaction groups
- unusual balance movements
- important changes from prior period if available
- plain-language explanation of what happened

### Internal receives
- explanation trace
- confidence by section
- missing data flags
- document quality impact
- statement coverage notes

### Required inputs
- statement metadata
- balances
- transaction rows
- dates
- transaction narration
- confidence fields
- optional prior-statement history

### Service dependencies
- OCR text extraction
- table extraction
- metadata extraction
- transaction normalisation
- explanation generator
- quality scorer

### Cost sensitivity
Low to medium

### Mandatory
Yes

---

## A2. Cash Flow Analysis Service

### Customer asks
- What is my cash flow?
- Am I cash positive or negative?
- Show inflows and outflows
- Show my monthly movement

### Customer options
- per statement
- monthly view
- rolling period view
- include charts
- include transaction type breakdown

### Customer receives
- inflow total
- outflow total
- net movement
- timing of inflows/outflows
- cash flow trend
- volatility and imbalance indicators

### Internal receives
- classified inflow/outflow objects
- quality score
- transaction inclusion/exclusion notes
- missing-period warnings

### Required inputs
- normalised transactions
- balance metadata
- transaction direction
- categorisation outputs
- date coverage

### Service dependencies
- transaction normaliser
- cash flow classifier
- balance behaviour engine
- trend engine

### Cost sensitivity
Medium

### Mandatory
Yes

---

## A3. Spending Analysis Service

### Customer asks
- Where is my money going?
- What do I spend most on?
- Am I overspending?
- Compare my spending across periods

### Customer options
- category breakdown
- merchant breakdown
- recurring spending only
- essential vs discretionary
- business vs personal if supported
- compare to prior period

### Customer receives
- spending by category
- top merchants / counterparties
- recurring spend
- discretionary vs committed spend
- unusual spending concentrations
- changes in spend between periods

### Internal receives
- category confidence
- merchant normalisation confidence
- transaction coverage stats
- distribution metrics

### Required inputs
- transaction rows
- semantic transaction categories
- merchant resolution
- recurring detection
- period groupings

### Service dependencies
- transaction semantic classifier
- spending behaviour classifier
- merchant/entity resolver
- distribution analysis engine
- frequency analysis engine

### Cost sensitivity
Medium

### Mandatory
Yes

---

## A4. Income Analysis Service

### Customer asks
- What income did I receive?
- Is my income stable?
- How regular is my salary or revenue?

### Customer options
- income only
- recurring income view
- multiple income source view
- stability over time
- compare across periods

### Customer receives
- identified income sources
- recurring income pattern
- timing consistency
- income variability
- reliability / regularity indicators

### Internal receives
- income classification confidence
- source grouping logic
- ambiguity flags
- missing-history constraints

### Required inputs
- transaction rows
- narration
- date patterns
- amounts
- history across statements if available

### Service dependencies
- income detection model
- recurring detector
- frequency analysis
- trend engine

### Cost sensitivity
Medium

### Mandatory
Yes

---

## A5. Indebtedness & Obligations Service

### Customer asks
- What debt obligations do I have?
- How much of my cash is going to debt?
- Am I overloaded?
- What are my recurring commitments?

### Customer options
- debt-only view
- debt + committed expenses
- affordability-style summary
- over time

### Customer receives
- identified debt repayments
- recurring obligations
- estimated debt burden
- commitment ratio
- pressure periods
- early overload indicators

### Internal receives
- obligation classification trace
- debt-related transaction confidence
- overlap with credit/collections domains
- risk markers

### Required inputs
- transaction rows
- recurring payments
- semantic categories
- counterparty classes
- balance behaviour

### Service dependencies
- indebtedness classification engine
- recurring detector
- counterparty classifier
- financial stress detector

### Cost sensitivity
Medium

### Mandatory
Yes

---

# B. Differentiation Services

## B1. Pricing / Cost Benchmarking Service

### Customer asks
- Am I paying too much?
- Are my fees / premiums / instalments high?
- Is my insurance high relative to my loan?
- Is my transport spend too high?

### Customer options
- compare against peer averages
- compare against own history
- compare against ratio benchmarks
- compare selected spend types only

### Customer receives
- benchmark comparison
- over/under average indicators
- ratio comparisons
- identified cost pressure items
- possible optimisation targets

### Internal receives
- benchmark source used
- confidence and applicability
- whether comparison is internal-population or external-market based
- exclusions and caveats

### Required inputs
- categorised transactions
- identified obligations
- benchmark dataset or external pricing source
- customer segment / profile if allowed

### Service dependencies
- semantic categories
- indebtedness classifications
- benchmark engine
- comparative analytics

### Cost sensitivity
Medium to high depending on data source

### Mandatory
No

### Strategic importance
Very high

---

## B2. Financial Behaviour Insights Service

### Customer asks
- What does my spending behaviour say?
- Where am I overspending?
- What habits are driving my financial outcomes?

### Customer options
- short explanation
- detailed behaviour report
- focus on one area
- trend-aware view

### Customer receives
- behavioural patterns
- recurring problem areas
- discretionary pressure areas
- changes in habits
- behaviour-linked insights

### Internal receives
- rule and model triggers
- behaviour classification trace
- confidence and caveat flags

### Required inputs
- categorised transactions
- frequency and distribution metrics
- period comparisons

### Service dependencies
- spending behaviour classifier
- frequency engine
- trend engine
- explanation generator

### Cost sensitivity
Medium

### Mandatory
No

---

## B3. Timing & Optimisation Service

### Customer asks
- What if I pay earlier?
- When am I most financially stretched?
- When is the best time to make payments?
- What is the cost impact of waiting?

### Customer options
- debt payment timing
- recurring expense timing
- short-term liquidity optimisation
- simple or advanced scenario mode

### Customer receives
- suggested timing windows
- impact estimates
- earlier/later payment comparisons
- short-term cash pressure projections

### Internal receives
- assumptions used
- sensitivity flags
- scenario model confidence
- dependency trace

### Required inputs
- transaction dates
- recurring obligations
- balances
- timing history
- optional forward assumptions

### Service dependencies
- timing optimisation engine
- balance behaviour engine
- recurring detector
- forecast / scenario model

### Cost sensitivity
High

### Mandatory
No

### Strategic importance
Very high

---

## B4. Financial Stress / Overload Detection Service

### Customer asks
- Am I overloaded?
- When do I become financially stressed?
- Am I nearing a problem point?

### Customer options
- current period only
- multi-period trend
- debt-weighted
- full financial stress view

### Customer receives
- overload indicators
- stress dates / periods
- pressure drivers
- severity band
- next-step guidance

### Internal receives
- trigger decomposition
- stress score components
- confidence and sufficiency markers
- escalation recommendations

### Required inputs
- cash flow
- obligations
- balances
- timing and trend metrics

### Service dependencies
- cash flow engine
- indebtedness engine
- financial stress model
- timing engine

### Cost sensitivity
Medium to high

### Mandatory
No

### Strategic importance
High

---

## B5. Anomaly & Fraud Insight Service

### Customer asks
- What looks unusual?
- Were there suspicious or abnormal transactions?
- Highlight anything inconsistent

### Customer options
- simple anomaly detection
- transaction anomaly only
- behaviour anomaly
- document inconsistency view

### Customer receives
- flagged anomalies
- severity and reason
- suspicious transaction list
- confidence and caution notes

### Internal receives
- anomaly model outputs
- supporting indicators
- rule hits
- escalation trace

### Required inputs
- transaction history
- distributions
- trends
- optional document integrity indicators

### Service dependencies
- anomaly detector
- fraud flags if available
- behaviour engine
- explanation generator

### Cost sensitivity
Medium to high

### Mandatory
No

---

# C. Platform Expansion Services

## C1. Proof & Verification Service

### Customer asks
- Show proof I paid
- Send proof to merchant / provider
- Confirm authenticity of this transaction / document

### Customer receives
- proof object
- verified extract
- transaction reference
- supporting statement evidence
- authenticity note / verification status

### Internal receives
- provenance trace
- document version used
- consent record
- share log

### Strategic importance
Very high

---

## C2. Document Vault Service

### Customer asks
- store my statements and supporting documents
- keep history for me
- retrieve prior proofs and reports

### Customer receives
- stored documents
- structured history
- searchable archive
- linked insights over time

### Internal receives
- document lineage
- version history
- storage status
- access and consent trace

### Strategic importance
Very high

---

## C3. Consent & Sharing Service

### Customer asks
- share my document or proof with a third party
- withdraw access
- approve use for a specific purpose

### Customer receives
- consent controls
- share logs
- purpose-bound access
- revoke capability

### Internal receives
- consent state
- access history
- policy trace

### Strategic importance
Very high

---

## C4. Trend & Financial Health Monitoring Service

### Customer asks
- keep me updated
- show whether I am improving
- alert me when my trends worsen

### Customer receives
- financial health trend
- improvement / deterioration indicators
- regular updates
- alerting

### Internal receives
- trend computation trace
- health score components
- refresh status

### Strategic importance
Very high

---

## C5. Wealth Creation / Planning Support Service

### Customer asks
- how can I improve my financial position?
- what should I change to build wealth?
- what is the impact of different choices?

### Customer receives
- improvement suggestions
- scenario comparisons
- financial behaviour opportunities
- optimisation insights

### Internal receives
- planning assumptions
- scenario model inputs
- suitability and limitation flags

### Strategic importance
High

---

## C6. Population Insights / Benchmark Engine

### Purpose
Use accumulated consented data to improve benchmarks, pricing comparisons, behavioural norms, and product intelligence.

### Strategic importance
Very high

### Delivery timing
Later phase, but architecture must allow it now

## 5. Cross-cutting service dimensions

Every Financial Management service should be tagged across these dimensions.

### Service execution mode
- mandatory
- optional
- premium
- internal-only
- future

### Customer complexity mode
- simple
- standard
- advanced
- advisor / internal

### Processing dependency mode
- OCR-direct
- OCR + deterministic transforms
- OCR + rules
- OCR + model/API enrichment
- multi-document / historical

### Confidence mode
- high confidence required
- partial allowed
- explanation required
- escalation required

### Cost mode
- low cost
- medium cost
- high cost
- run only if justified

## 6. Front-end implications

### Customer-facing view must support
- summaries
- explanations
- trends
- comparisons
- alerts
- proof requests
- stored history

### Internal-facing view must support
- quality
- confidence
- component scores
- service sufficiency
- model trace
- exceptions
- consent / audit state

## 7. Immediate design consequences

1. We cannot design a single Financial Management payload.
2. We need multiple classification layers, not one.
3. We need the decision engine to decide:
   - what is mandatory
   - what is optional
   - what is too costly
   - what is unsupported due to insufficient evidence
4. The OCR side only needs to deliver the structured evidence base required by these services.

## 8. Document purpose

This service menu is:
- the product contract
- the architecture driver
- the basis for model catalog refinement
- the basis for front-end page and API design
- the basis for decision-engine design
- the basis for OCR input/output requirement derivation
