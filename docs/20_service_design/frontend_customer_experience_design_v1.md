# Frontend Customer Experience Design Baseline v1

## 1. PURPOSE

This document defines the authoritative frontend customer experience design baseline for the platform.

It governs:
- User experience design
- Frontend interaction patterns
- Page structure and behaviour
- User journey logic

Scope:
- Customer-facing frontend only
- Applies to all personas and journeys
- Applies across personal, business, and operational usage

This document defines WHAT MUST BE, not current implementation.

## 2. DESIGN PRINCIPLES

The frontend must adhere to the following enforced principles:

### Explain-before-input
No data or document input is requested without first explaining:
- what is required
- why it is required
- what will happen next

### Trust-first design
Trust is continuously reinforced through:
- messaging
- layout
- visual cues
- interaction clarity

### Progressive disclosure
- Start simple
- Reveal complexity only when needed

### Dual-mode UX
- Guided mode (default)
- Efficient mode (repeat/advanced users)

### Context identity (always visible)
System must always show:
- user
- context (personal/business)
- business (if applicable)
- client (if applicable)
- service

### Supportive error and recovery model
Errors must be:
- non-accusatory
- assistive
- actionable

### Upload as guided journey
Upload is not a field. It is:
- explained
- validated
- recoverable

### Clarity to Trust to Action
All flows must follow:
1. clarity
2. trust
3. action

## 3. PERSONA MODEL (STEP 1)

### Segmentation dimensions

- User type (personal, SME, enterprise, admin, ops, compliance)
- Digital literacy
- Financial literacy
- Registration state (anonymous, first-time, repeat)
- Intent (test vs real use)
- Lifecycle stage

### Personas

#### Personal users
- Low literacy
- Moderate users
- Financially astute users

#### Business users
- SME (low complexity, similar to personal)
- Enterprise (structured, high complexity)

#### Cross-cutting states
- Non-registered users
- Registered first-time users
- Repeat users

#### Internal users
- Operational and support
- Billing and admin
- Compliance and risk

### South African constraints

- Mobile-first usage
- Uneven digital literacy
- High fraud sensitivity
- Multilingual context
- Cost sensitivity

## 4. UX PATTERN FOUNDATION (STEP 2)

### Best-practice patterns

- Early user path separation
- Outcome-based CTAs
- Step-by-step flows
- Inline validation
- Continuous feedback
- Trust messaging embedded throughout

### Failure patterns

- Generic entry points
- No explanation before input
- Poor upload guidance
- Long unstructured forms
- No progress visibility
- Hidden trust signals

### Enforced UX rules

- No single funnel for all users
- Upload must be guided
- Trust must be visible throughout
- Progress must always be visible

## 5. USER JOURNEYS (STEP 3)

### Entry points

- Understand a document
- Submit documents
- Business and organisation
- Test and explore

### Journey types

#### Personal (guided and efficient)
#### SME business
#### Enterprise business
#### Test and exploration

### Context identity layer

Always visible:
- user
- context
- business
- client
- service

### Upload sub-journey

Includes:
- explanation
- example
- upload
- validation
- recovery
- confirmation

### Error and recovery model

Includes:
- identity mismatch
- duplicate submission
- wrong client
- invalid document
- wrong document type

All errors must:
- explain
- guide
- offer options

### Resume and interruption model

System must:
- show what is being resumed
- confirm context
- allow continue, restart, or switch

## 6. INFORMATION ARCHITECTURE (STEP 4)

### Page layers

1. Public and SEO
2. Guided entry
3. Workflow
4. Account and operational

### Page inventory

#### Public
- Homepage
- Service pages
- Trust and security
- How it works
- Help and support

#### Guided entry
- Entry selection
- Service selection
- Requirement explanation

#### Workflow
- Context setup
- Document selection
- Upload
- Review
- Submit
- Results
- Resume

#### Business
- Client selection
- Service catalogue
- Dashboard

#### Account
- Account dashboard
- Billing
- User management
- Support
- Audit and history

### SEO vs workflow separation

SEO pages:
- educate
- build trust
- route users

Workflow pages:
- execute tasks

## 7. LOOK AND FEEL / DESIGN SYSTEM (STEP 5)

### Colour system

- Primary: trust (blue)
- Neutral: background (grey/white)
- Accent: action
- Functional colours:
  - success (green)
  - warning (amber)
  - error (red)

### Visual tone

- clean
- calm
- non-intimidating
- structured

### Layout system

Standard page:
1. Header
2. Context strip
3. Content
4. Action
5. Support

### Context strip (formal component)

Displays:
- user
- context
- business
- client
- service

Always visible and persistent.

### Upload module

Includes:
- explanation
- example
- upload area
- validation
- recovery

### Error and recovery design

Must show:
- issue
- explanation
- options

### Progress indicators

Must show:
- current step
- remaining steps

### Typography

- simple
- readable
- mobile-first
- minimal jargon

### Mobile-first behaviour

- vertical layouts
- large touch targets
- minimal typing
- camera-based upload

### Accessibility

- high contrast
- simple language
- icon and text pairing
- not colour-dependent

## 8. DESIGN CONSTRAINTS

The following are non-negotiable:

- No mixed-purpose pages
- No input before explanation
- Upload must be guided
- Context must always be visible
- One primary purpose per page
- One primary action per page
- No hidden steps
- No assumption of user knowledge

## 9. TRACEABILITY

| Step | Output | Where Used |
|------|--------|-----------|
| Step 1 | Persona model | Journeys, IA, design decisions |
| Step 2 | UX patterns | Design principles, flows |
| Step 3 | User journeys | Page design, workflow logic |
| Step 4 | IA | Page structure |
| Step 5 | Design system | UI and visual design |

## 10. WHAT THIS DOCUMENT IS NOT

This document is NOT:
- Implementation guidance
- Code specification
- Current frontend state
- Temporary design iteration

This document defines:
Authoritative design truth (WHAT MUST BE)
