# Frontend Page-by-Page Journey Design v1

## Status
DRAFT FOR DESIGN SIGN-OFF
NO IMPLEMENTATION UNTIL APPROVED

## 1. Purpose
Define the complete governed frontend journey before further coding.

## 2. Required Design Completion Questions

For every page we must define:
- page name
- page purpose
- what is shown
- what context is always visible
- what inputs are captured
- what service-specific rules apply
- what validations apply
- what conditions allow continue
- what back navigation is allowed
- what resume behavior applies
- what happens after logout/login
- what system data vs user data is required
- what errors/recovery options are shown
- what progress indicator must show

## 3. Pages To Define
1. Entry
2. Service Selection
3. Context Setup
4. Document Selection
5. Upload
6. Validation / Recovery
7. Review
8. Submit
9. Results
10. Resume

## 4. Cross-Cutting Design Areas Still Requiring Definition
- user / client / business context strip
- request resume model
- page revisit rules
- service-specific required user inputs
- document grouping / batching model
- upload method model
- completeness checks
- quality guidance
- waiting / progress / communication model

## 5. Design Rule Alignment
Must align to governed rules:
- no mixed-purpose pages
- no input before explanation
- upload must be guided
- context must always be visible
- one primary purpose per page
- one primary action per page
- no hidden steps

## 6. Approval Rule
No more frontend journey coding until this document is completed and approved.


## 7. Page Definition Template

For each page, complete this structure:

### Page Name

**Primary purpose**
- 

**What is shown**
- 

**Context always visible**
- 
- 
- 

**Inputs captured**
- 

**Service-specific rules**
- 

**Validation rules**
- 

**Continue conditions**
- 

**Back navigation**
- 

**Resume behavior**
- 

**Logout/login return behavior**
- 

**Errors and recovery**
- 

**Progress indicator**
- current step:
- remaining steps:

---

## 8. Pages To Complete First

### Entry

**Primary purpose**
- Route the signed-in user into the correct governed journey start.

**What is shown**
- Available entry actions
- Resume option if there is an active journey
- Trust / explanation text

**Context always visible**
- signed-in user
- current client / business context if applicable

**Inputs captured**
- entry action only

**Service-specific rules**
- none at this stage

**Validation rules**
- user must choose a valid entry path

**Continue conditions**
- entry action selected

**Back navigation**
- back to landing/home allowed

**Resume behavior**
- if an in-progress journey exists, show resume choice

**Logout/login return behavior**
- must define whether default is landing page or resumable journey

**Errors and recovery**
- show invalid or unavailable path clearly
- offer alternate route

**Progress indicator**
- current step: Entry
- remaining steps: Service Selection, Context Setup, Document Selection, Upload, Review, Submit, Results

### Service Selection

**Primary purpose**
- Select the exact governed backend service / outcome-intent to execute.

**What is shown**
- service catalogue grouped clearly
- explanation of each selectable service
- one primary action only

**Context always visible**
- signed-in user
- current client / business context
- selected journey type if already known

**Inputs captured**
- serviceCode
- analysisType

**Service-specific rules**
- only governed selectable services may appear
- no fake categories as executable choices

**Validation rules**
- valid service must be selected

**Continue conditions**
- service selected

**Back navigation**
- allowed to Entry

**Resume behavior**
- show selected service if resuming

**Logout/login return behavior**
- must define whether selected service is restored automatically

**Errors and recovery**
- unavailable service must explain why
- allow reselection

**Progress indicator**
- current step: Service Selection
- remaining steps: Context Setup, Document Selection, Upload, Review, Submit, Results

### Context Setup

**Primary purpose**
- Capture the governing request context before document upload.

**What is shown**
- whose documents are being worked on
- whether context is individual or business
- selected service
- required request structure for that service

**Context always visible**
- signed-in user
- client / business
- selected service

**Inputs captured**
- subject type (individual / business)
- any required service request metadata not provided by documents
- upload grouping / batching method if needed

**Service-specific rules**
- context questions must vary by selected service
- only ask for inputs actually required for the selected service

**Validation rules**
- all mandatory context fields complete

**Continue conditions**
- context complete and valid

**Back navigation**
- allowed to Service Selection

**Resume behavior**
- restore prior answers

**Logout/login return behavior**
- must restore current context if journey is resumable

**Errors and recovery**
- explain missing or conflicting context
- allow correction

**Progress indicator**
- current step: Context Setup
- remaining steps: Document Selection, Upload, Review, Submit, Results

### Document Selection

**Primary purpose**
- Select the required document types for the already-defined context and service.

**What is shown**
- required document types
- optional document types if governed
- repeatable document groups if applicable
- explanation before selection

**Context always visible**
- signed-in user
- client / business
- selected service
- subject context

**Inputs captured**
- document types to be uploaded
- document grouping expectations if needed

**Service-specific rules**
- document options must be derived from selected service and context
- multi-document and multi-period cases must be defined per service

**Validation rules**
- all required document types selected
- incompatible combinations blocked

**Continue conditions**
- required document selection complete

**Back navigation**
- allowed to Context Setup

**Resume behavior**
- restore prior document choices

**Logout/login return behavior**
- must restore current document selection if journey is resumable

**Errors and recovery**
- explain missing required document types
- allow correction

**Progress indicator**
- current step: Document Selection
- remaining steps: Upload, Review, Submit, Results

### Upload

**Primary purpose**
- Execute the guided upload sub-journey for the selected service, context, and document set.

**What is shown**
- explanation of what to upload
- example of acceptable upload structure
- upload area
- file grouping / batching instructions
- progress within upload if multiple batches are required

**Context always visible**
- signed-in user
- client / business
- selected service
- subject context
- selected document set

**Inputs captured**
- uploaded file(s)
- upload grouping choice if not already captured
- file type / batch association where needed

**Service-specific rules**
- upload model must vary by service and document set
- support single file, multiple files, multi-period, and mixed-format cases where governed

**Validation rules**
- accepted file types only
- required batches / files present
- invalid file combinations blocked
- upload completeness checked before continue

**Continue conditions**
- required upload set present
- upload structure valid

**Back navigation**
- allowed to Document Selection unless files would be discarded, in which case warn

**Resume behavior**
- show already uploaded batches / files
- allow continue or replace where governed

**Logout/login return behavior**
- restore uploaded-state view if resumable
- clearly show what is already uploaded

**Errors and recovery**
- invalid file type
- missing required batch
- failed upload
- re-upload / replace option
- explanation and recovery path required

**Progress indicator**
- current step: Upload
- remaining steps: Validation / Recovery, Review, Submit, Results

### Validation / Recovery

**Primary purpose**
- confirm uploaded material is structurally ready before review and submit.

**What is shown**
- upload validation results
- completeness status
- grouping / batching validation
- quality guidance hooks
- recovery actions

**Context always visible**
- signed-in user
- client / business
- selected service
- subject context
- uploaded document set summary

**Inputs captured**
- re-upload decision
- replace file decision
- continue after validation success

**Service-specific rules**
- validation must reflect service-specific document expectations
- multi-period and multi-document completeness must be checked where relevant

**Validation rules**
- required files present
- required document groups present
- grouping consistent with declared upload method
- no continue on blocking validation failures

**Continue conditions**
- no blocking validation failures remain

**Back navigation**
- allowed to Upload

**Resume behavior**
- restore validation status and recovery options

**Logout/login return behavior**
- return user to current validation state if resumable

**Errors and recovery**
- must show issue
- explanation
- options
- re-upload / replace path

**Progress indicator**
- current step: Validation / Recovery
- remaining steps: Review, Submit, Results

### Review

**Primary purpose**
- let the user confirm exactly what will be submitted.

**What is shown**
- selected service
- subject context
- selected document types
- uploaded document summary
- key request inputs captured so far
- declarations / confirmations still required

**Context always visible**
- signed-in user
- client / business
- selected service
- subject context

**Inputs captured**
- final confirmation inputs required before submit
- declaration acknowledgement

**Service-specific rules**
- review content must reflect selected service and actual uploaded set

**Validation rules**
- all mandatory confirmations complete
- no unresolved validation blockers

**Continue conditions**
- review accepted
- declarations completed

**Back navigation**
- allowed to Validation / Recovery or Upload depending on what needs correction

**Resume behavior**
- restore prior review state and confirmations if allowed

**Logout/login return behavior**
- must restore review state if resumable

**Errors and recovery**
- show missing confirmations clearly
- route user back to the correct correction step

**Progress indicator**
- current step: Review
- remaining steps: Submit, Results

### Submit

**Primary purpose**
- commit the prepared request into the governed backend process.

**What is shown**
- submission summary
- what happens next
- final primary action only

**Context always visible**
- signed-in user
- client / business
- selected service
- subject context
- request summary

**Inputs captured**
- final submit action only

**Service-specific rules**
- submit payload must match governed backend contract for selected service

**Validation rules**
- no unresolved blockers
- all required confirmations complete
- request payload complete

**Continue conditions**
- successful request creation

**Back navigation**
- allowed back to Review until submit occurs
- after submit, editing must stop unless restart is governed

**Resume behavior**
- if not yet submitted, return to Review / Submit state
- if already submitted, redirect to Results / Resume

**Logout/login return behavior**
- must resume pending submit state or submitted request state correctly

**Errors and recovery**
- request creation failure
- document upload/linking failure
- clear retry / support path

**Progress indicator**
- current step: Submit
- remaining steps: Results

### Results

**Primary purpose**
- show the current request outcome / status and next available action.

**What is shown**
- request identifier
- current status
- selected service
- uploaded document summary
- result / awaiting-processing message
- support / history entry points

**Context always visible**
- signed-in user
- client / business
- selected service
- request identifier

**Inputs captured**
- no mandatory inputs
- optional follow-up actions only

**Service-specific rules**
- result presentation must match service type and backend status

**Validation rules**
- results page must only show for a valid created request

**Continue conditions**
- none; this is an outcome/status page

**Back navigation**
- back to prior editable pages should not be allowed if request is already submitted

**Resume behavior**
- re-open existing request state and latest status

**Logout/login return behavior**
- return to resumable request / results view from dashboard or resume entry

**Errors and recovery**
- missing request
- invalid request access
- failed result retrieval
- show support path

**Progress indicator**
- current step: Results
- remaining steps: none

### Resume

**Primary purpose**
- help the user safely continue an interrupted journey without confusion.

**What is shown**
- what request / journey is being resumed
- selected service
- client / business context
- last completed step
- available actions: continue, restart, switch if governed

**Context always visible**
- signed-in user
- client / business
- selected service
- request / draft identifier

**Inputs captured**
- resume decision
- restart decision
- switch decision if allowed

**Service-specific rules**
- resume must restore the correct service-specific path and context

**Validation rules**
- resumable state must still be valid
- expired / blocked states must be handled explicitly

**Continue conditions**
- user chooses valid resume action

**Back navigation**
- back to Entry or dashboard if user does not resume

**Resume behavior**
- this page is the resume control point

**Logout/login return behavior**
- if a resumable journey exists, system must define whether to land here automatically or offer it from Entry

**Errors and recovery**
- expired draft
- invalid resume state
- conflicting context
- explain options clearly

**Progress indicator**
- current step: Resume
- remaining steps: depends on restored step

## 9. Trust and Reassurance Layer (MANDATORY)

The journey must subtly and continuously convey trust without clutter.

### Trust signals to define formally
- documents are stored securely
- encryption / vault positioning
- consent-based processing
- regulatory compliance
- auditability / traceability
- who the user is
- whose documents are being handled
- what service is being requested
- current step and remaining steps
- safe recovery / resumability

### Trust signal placement rules
For each page we must specify:
- persistent trust signals
- contextual trust signals
- waiting-state trust signals
- submission-state trust signals

### Minimum persistent trust strip
Must define whether the following are always visible on workflow pages:
- signed-in user
- acting for individual / business / client
- selected service
- consent / secure processing reminder
- progress indicator

### Upload trust requirements
Upload-related pages must explicitly reassure the user about:
- secure storage
- controlled processing
- consent basis
- what happens after upload
- what to do if quality or completeness fails

### Review / Submit trust requirements
Review and submit pages must explicitly reassure the user about:
- what exactly is being submitted
- that submission is governed and traceable
- what happens next
- where the user can later find the request

### Results / Resume trust requirements
Results and resume pages must clearly show:
- request identity
- status
- what is resumable
- what is already safely stored
- support / history path

### Approval rule
No page is design-complete until its trust and reassurance behavior is defined.

## 10. Navigation and Journey Control Model (MANDATORY)

The system must explicitly define how users move through the journey.

### Navigation rules to define

For every page:
- can user go back?
- can user skip forward?
- can user jump to a specific step?
- what happens if required data is missing?
- what happens if state becomes invalid?

### Back navigation

Must define:
- allowed backward steps per page
- whether data is retained or cleared when going back
- when warning must be shown before data loss

### Forward navigation

Must enforce:
- no skipping required steps
- continue only when validation conditions are met
- no hidden steps

### Direct navigation (URL access)

Must define:
- what happens if user navigates directly to:
  - upload
  - review
  - submit
- system must:
  - redirect to correct step
  - or reconstruct valid state

### Resume model (critical)

Must define:
- how the system determines last valid step
- what state must be stored to support resume
- whether resume happens automatically or via prompt

### Logout / login behavior

Must define:
- default landing page after login:
  - entry OR resume
- whether system:
  - auto-resumes last journey
  - prompts user to resume or start new

### Multi-request handling

Must define:
- whether user can have multiple active requests
- how they choose which to resume
- how context is separated

### Invalid state handling

Must define:
- missing required context
- missing document selection
- incomplete upload
- failed validation

System must:
- prevent progression
- explain issue
- route to correct recovery step

### Submission boundary

Must define:
- after submit:
  - no editing of prior steps
  - user moves to results/resume only
- system must enforce immutability of submitted request

### Progress model

Must define:
- visible step tracker
- current step
- remaining steps
- completed steps

### Approval rule

No journey implementation may proceed until navigation and control behavior is fully defined and approved.

## 11. Service Input Responsibility Model (MANDATORY)

Before implementation, every service / outcome-intent must define:

### Input ownership classes
- user-supplied inputs
- document-supplied inputs
- system / configuration supplied inputs

### For each selectable service, define:
- serviceCode
- analysisType / outcome-intent
- required user inputs
- optional user inputs
- required document types
- optional document types
- repeatable document groups
- whether subject context is required
- whether business context is required
- whether multi-period upload is supported
- whether mixed-format upload is supported

### Approval rule
No service may appear in the frontend until this matrix is complete.

## 12. Persistent Context Strip Model (MANDATORY)

Every workflow page must define exactly what stays visible at all times.

### Candidate fields
- signed-in user
- acting for: individual / business / client
- request / draft identifier
- selected service
- selected document set
- consent / secure processing reminder
- current step / remaining steps

### Approval rule
No workflow page is complete until its persistent context strip is defined.

## 13. Continue Conditions Matrix (MANDATORY)

For every page, define:

- required prior state
- required current inputs
- blocking validation failures
- continue allowed yes/no
- redirect rule if state invalid
- back-navigation rule
- resume-entry rule

### Approval rule
No journey page may be implemented without an explicit continue-condition definition.

## 14. Derived Frontend Behaviour (FROM MATRIX)

This section converts the service input matrix into actual frontend behaviour.

### 14.1 Context Setup Derivation

Context page must:

Show:
- selected service
- acting for: individual or business (only if required by service)
- any required subject fields (only where matrix indicates)

Rules:
- only ask for subject details when subject_context_required = yes
- only ask for business details when business_context_required = yes
- never ask for inputs that are document-derived

---

### 14.2 Document Selection Derivation

Document selection page must:

Show:
- required_document_types (mandatory)
- optional_document_types (if any)
- grouping explanation if repeatable_document_groups = yes

Rules:
- block continue until all required document types are selected
- allow multiple selections where repeatable = yes
- reflect service-specific combinations (e.g. payslip + bank statement)

---

### 14.3 Upload Model Derivation

Upload page must adapt per matrix:

If repeatable_document_groups = yes:
- allow multiple uploads per document type

If multi_period_supported = yes:
- allow grouping by period (user-defined or guided)

If mixed_format_supported = yes:
- allow PDF + images in same submission

Upload patterns supported:
- single file
- multiple files
- grouped batches (per document type or period)

---

### 14.4 Validation Rules Derivation

Validation page must enforce:

- required_document_types present
- grouping consistent with declared upload structure
- no missing mandatory document sets
- no invalid combinations

---

### 14.5 Service-Specific Behaviour Summary

OCR:
- single generic document
- no subject context
- simple upload

FICA:
- identity / proof of address / business registration
- subject context required in some cases
- business vs individual affects document type

Credit Decision:
- payslip + bank statement
- multi-period required
- strong grouping and completeness validation

Financial Management:
- primarily bank statements
- multi-period
- analytics-driven outcomes

---

### Approval Rule

Frontend behaviour is now fully derived.

No further interpretation required during implementation.

## 15. Design Lock Decision

Status: DESIGN LOCKED FOR IMPLEMENTATION

The frontend journey design is now considered complete enough for controlled implementation.

Completed design elements:
- page-by-page journey
- trust and reassurance layer
- navigation and journey control model
- service input responsibility model
- derived frontend behaviour from service matrix

Implementation rule:
- code must now follow this design
- no further journey behaviour changes without updating this design first
- implementation must proceed page-by-page against this document

Next implementation order:
1. Context Setup page
2. Document Selection page
3. Guided Upload page
4. Validation / Recovery page
5. Review page
6. Submit page
7. Results / Resume page
