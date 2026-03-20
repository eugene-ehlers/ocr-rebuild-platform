# Front-End / Control Plane — API Surface v1

## 1. Purpose

Defines all API domains exposed by the Front-End / Control Plane.

All APIs must be:
- authenticated
- authorized
- auditable
- versioned

---

## 2. API Domains

---

### 2.1 Identity & Admin APIs

- POST /api/v1/auth/register/personal
- POST /api/v1/auth/register/business
- POST /api/v1/auth/login
- POST /api/v1/auth/logout

- GET /api/v1/admin/users
- POST /api/v1/admin/users
- PUT /api/v1/admin/users/{id}
- DELETE /api/v1/admin/users/{id}

---

### 2.2 Consent APIs

- POST /api/v1/consent/capture
- GET /api/v1/consent/{id}
- POST /api/v1/consent/revoke
- GET /api/v1/consent/validate

---

### 2.3 Document APIs

- POST /api/v1/documents/upload
- GET /api/v1/documents/{id}
- PUT /api/v1/documents/{id}/replace
- POST /api/v1/documents/{id}/append
- POST /api/v1/documents/{id}/reorder
- GET /api/v1/documents/{id}/validate

---

### 2.4 Request & Results APIs

- GET /api/v1/services
- POST /api/v1/requests
- GET /api/v1/requests/{id}
- GET /api/v1/results/{id}
- POST /api/v1/requests/{id}/rerun

---

### 2.5 Annotation APIs

- POST /api/v1/annotations
- GET /api/v1/annotations/{id}
- PUT /api/v1/annotations/{id}
- POST /api/v1/annotations/{id}/submit

---

### 2.6 Operational Admin APIs

- GET /api/v1/admin/balance
- POST /api/v1/admin/payment (simulated)
- GET /api/v1/admin/usage
- GET /api/v1/admin/activity

---

### 2.7 Support APIs

- POST /api/v1/support/request
- GET /api/v1/support/{id}
- POST /api/v1/support/respond (placeholder)

---

### 2.8 Telemetry APIs

- POST /api/v1/telemetry/event
- POST /api/v1/telemetry/workflow
- GET /api/v1/telemetry/export (internal)

---

## 3. Principles

- APIs must not contain business logic of downstream services
- APIs orchestrate and route
- APIs must enforce consent before execution
- APIs must log all critical actions

