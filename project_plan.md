Perfect combo! Here's a project sized just right for 2 months, full stack, Python backend, SaaS-style, and deep enough to cover all the standards you want.

---

## 🚀 Project: **FormCraft — A SaaS Form Builder & Response Collector**

Think a lightweight **Typeform/Google Forms clone** — users sign up, create custom forms, share a public link, collect responses, and view analytics. Simple concept, but the engineering underneath is genuinely meaty.

---

## Why This Project?

- **Real-world SaaS patterns**: auth, multi-tenancy, public vs private routes
- **Rich AWS service usage** across compute, storage, messaging, and CDN
- **Data-heavy enough** to practice DynamoDB design seriously
- **Event-driven architecture** opportunity (form submission → async processing)
- **Frontend + Backend** both have meaningful work

---

## Architecture (Free Tier)

| Service | Role | Free Limit |
|---|---|---|
| **Lambda (Python)** | API logic, form CRUD, response handling | 1M req/month |
| **API Gateway** | REST endpoints | 1M calls/month |
| **DynamoDB** | Forms, responses, users (single-table design) | 25 GB |
| **S3** | File uploads in forms (images/PDFs), frontend hosting | 5 GB |
| **CloudFront** | CDN for frontend + presigned URL delivery | 1 TB out |
| **Cognito** | User auth (sign up, login, JWT) | 50,000 MAU free |
| **SQS** | Async response processing queue | 1M requests/month |
| **SES** | Email notifications on form submission | 3,000 emails/month |
| **CloudWatch** | Logs, alarms, dashboards | 10 alarms free |
| **SSM Parameter Store** | Secrets per environment | Free tier |

---

## Core Features to Build

**Auth layer**
- Sign up / login via Cognito
- JWT-protected API routes

**Form Builder (Backend)**
- Create / update / delete forms
- Field types: text, dropdown, checkbox, file upload
- Toggle form active/inactive

**Public Form (Respondent side)**
- Anyone with the link can submit
- File uploads go directly to S3 via presigned URLs
- Submission triggers an SQS message → Lambda processes async

**Response Dashboard**
- View all responses per form
- Basic analytics: total responses, completion rate, field-level breakdown
- CSV export of responses

**Notifications**
- SES email to form owner on every new submission

---

## 2-Month Roadmap

### Week 1–2 — Foundation
- AWS account hardening (MFA, IAM users, billing alarm)
- Terraform remote state: S3 + DynamoDB lock
- Scaffold repo structure (monorepo: `/infra`, `/backend`, `/frontend`)
- Cognito user pool via Terraform
- `dev` environment deployed

### Week 3–4 — Core Backend
- DynamoDB single-table design (forms + responses + users in one table)
- Lambda functions: form CRUD, response submit
- API Gateway with Cognito authorizer
- S3 presigned URL generation for file uploads
- Local testing with AWS SAM CLI

### Week 5 — Frontend
- React + Tailwind (hosted on S3 + CloudFront)
- Auth flows (login, signup, protected routes)
- Form builder UI (drag-and-drop optional, manual order fine)
- Public form page (no auth required)

### Week 6 — Async + Notifications
- SQS queue wired to form submission Lambda
- SES email notification on submission
- Response dashboard with basic charts (Chart.js)
- CSV export endpoint

### Week 7 — Multi-env + CI/CD
- Terraform modules finalized (`dev`, `staging`, `prod`)
- Lambda aliases per environment
- GitHub Actions: `develop` → dev, `main` → staging → manual gate → prod
- `terraform plan` as PR comment

### Week 8 — Observability + Polish
- CloudWatch dashboard: submissions/hour, Lambda errors, SQS queue depth
- Alarms: error rate spike → SNS → email alert
- DR drill: restore DynamoDB table from PITR
- Architecture diagram + polished README
- Cost audit of your AWS bill

---

## Repo Structure
```
/formcraft
  /infra
    /modules
      /lambda
      /dynamodb
      /cognito
      /api-gateway
      /sqs
    /environments
      /dev
      /staging
      /prod
  /backend
    /functions
      /form-crud
      /response-handler
      /notification-sender
      /export
    /shared
      /db.py
      /auth.py
  /frontend
    /src
      /pages
      /components
      /hooks
```

---

## What Makes This Portfolio-Worthy

By the end you'll have demonstrated:

- **Multi-tenant SaaS** auth with Cognito
- **Event-driven** async processing with SQS + Lambda
- **Single-table DynamoDB** design (the hardest NoSQL skill to show)
- **IaC** with reusable Terraform modules across 3 environments
- **CI/CD** with approval gates
- **Observability** with real alarms and dashboards
- **Full stack** — React frontend, Python backend, cloud infra

That's a project you can talk about for 30 minutes in any backend, cloud, or full stack interview.

---

Want me to start with the **Terraform folder scaffold**, the **DynamoDB single-table schema**, or the **GitHub Actions workflow**?