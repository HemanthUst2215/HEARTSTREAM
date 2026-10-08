# Infrastructure Deployment — {{ENVIRONMENT_OR_STACK}}

> From `/generate-infra`. infra-agent owns Terraform/cloud and GitHub Actions. No broad IAM without escalate.

| Field | Value |
|-------|-------|
| **Deployment ID** | INFRA-{{YYYYMMDD}}-{{slug}} |
| **Environment** | dev / staging / prod |
| **Region** | {{cloud region}} |
| **Owner** | infra-agent |
| **Story / NFR refs** | {{ids}} |
| **Status** | Planned / Applied / Failed / Rolled back |

## Objectives

- **Resources to provision/update:**
- **Dependencies:**

## Architecture diagram

```text
(describe or link to diagram)
```

## Resource inventory

| Resource type | Name | Purpose | Module path |
|---------------|------|---------|-------------|
| | | | `${modules.infra}/…` |

## IAM summary

| Role / identity | Permissions | Justification | Least privilege verified |
|-----------------|-------------|---------------|--------------------------|
| | | | yes/no |

## Secrets and config

| Secret name | Store (Key Vault / SM) | Rotation | In code? |
|-------------|------------------------|----------|----------|
| | | | must be NO |

## CI/CD workflow

| Workflow file | Trigger | Steps summary |
|---------------|---------|---------------|
| `.github/workflows/…` | push / manual | |

## Deployment steps

| # | Step | Command / pipeline | Rollback |
|---|------|-------------------|----------|
| 1 | Plan | `terraform plan` | |
| 2 | Apply | | `terraform apply -destroy` scope |

## Validation

| Check | Method | Expected |
|-------|--------|----------|
| Health | | |
| Smoke test | | |

## Open items / escalations

| ID | Item | Owner |
|----|------|-------|
| | Broad IAM needs approval | |

**Output path:** `docs/infra/{{env}}-{{slug}}-deployment.md` and `${modules.infra}/`
