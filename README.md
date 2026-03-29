# Bu-uelo Y Tinto — Event Store Backend

Backend API and AWS infrastructure for a live event sales platform (food & drinks ordering). Built as a university architecture course project with a focus on real cloud infrastructure, DDD backend design, and containerized deployment.

---

## Infrastructure overview

Fully provisioned with Terraform on AWS (`iac/`). The stack runs two EC2 instances behind a Network Load Balancer, pulling Docker images from ECR and connecting to a managed RDS PostgreSQL database.

```
Internet
    │
    ▼
AWS Network Load Balancer  (aws_lb — TCP:80)
    │              │
    ▼              ▼
EC2 t2.micro   EC2 t2.micro       ← 2 AZs, public subnets
(Docker)       (Docker)
    │              │
    └──────┬───────┘
           ▼
    RDS PostgreSQL 15   (db.t3.micro, private subnet group)

Supporting resources:
  ECR          ← container registry (frontend + backend repos)
  S3           ← config bucket (docker-compose.yml delivery at boot)
  IAM roles    ← EC2 → ECR pull, EC2 → S3 read
  SSM          ← chaos engineering hook (ssm_chaos.tf, ready to enable)
```

### Terraform modules (`iac/`)

| File | Resources |
|---|---|
| `main.tf` | Provider, ECR repos, IAM role + instance profile |
| `vpc.tf` | VPC, Internet Gateway, 2 public subnets, route table |
| `ec2.tf` | Security groups, 2 EC2 instances with user_data bootstrap |
| `lb.tf` | NLB, target group, listeners, instance attachments |
| `rds.tf` | RDS PostgreSQL 15, subnet group, security group |
| `s3.tf` | Config bucket, ownership controls, public access block |
| `ssm_chaos.tf` | SSM role + chaos injection document (commented, ready to activate) |
| `variables.tf` | VPC CIDRs, subnet CIDRs, DB credentials |
| `outputs.tf` | NLB DNS name |

**EC2 bootstrap flow:** On launch, each instance installs Docker + docker-compose, pulls `docker-compose.yml` from S3, logs into ECR, and starts the application stack — fully automated, no manual SSH required.

---

## Backend architecture

Django REST API structured with Domain-Driven Design (DDD):

```
src/lib/
  Customer/
    domain/          ← Customer entity, repository interface, specification
    application/     ← CustomerCreate, CustomerFind use cases
  Order/
    domain/          ← Order entity, DeliveryLocation value object
    application/     ← OrderCreate, OrderFind, OrderUpdate use cases
    infrastructure/  ← Django-specific request mapping
  OrderStatus/
    domain/          ← OrderStatus entity + repository
  Product/
    domain/          ← Product entity + specification
    application/     ← ProductFind use case
  Shared/
    domain/          ← Base classes, value objects, result types, specifications
    infrastructure/  ← MongoDB connection, schema base, exception handlers
```

**Key patterns used:**
- Value objects with validation (`BaseEmail`, `BasePrice`, `BaseUUID`, etc.)
- Repository interfaces decoupled from infrastructure
- Command/Query result types (`BaseCommandResult`, `BaseQueryResult`)
- Specification pattern for query filtering (`BaseCriteria`)

---

## Stack

`Python` `Django` `PostgreSQL 15` `Docker` `Terraform` `AWS EC2` `AWS RDS` `AWS NLB` `AWS ECR` `AWS S3` `AWS IAM` `AWS SSM`

---

## Project structure

```
iac/                    # Terraform — full AWS infrastructure
app/                    # Django app layer (views, serializers, URLs)
src/lib/                # DDD domain: entities, use cases, value objects
infrastructure/         # Django ORM models + migrations
domain/                 # Domain stubs (entities, services, value objects)
config/                 # Django settings, WSGI, URL root
Dockerfile              # Container build
docker-compose.yml      # Local + EC2 runtime
requirements.txt
```

---

## Quickstart (local)

```bash
git clone https://github.com/acarmonag/Bu-uelo-Y-Tinto
cd Bu-uelo-Y-Tinto
```

Set environment variables in `docker-compose.yml` or a `.env` file:
```
DB_HOST=localhost
DB_NAME=appdb
DB_USER=postgres
DB_PASSWORD=yourpassword
```

```bash
docker-compose up --build
```

API available at `http://localhost:8000`.

---

## Infrastructure deployment

> Requires AWS CLI configured and Terraform installed.

```bash
cd iac
terraform init
terraform plan
terraform apply
```

The NLB DNS name is output after apply:
```
nlb_dns_name = "web-nlb-xxxx.elb.us-east-1.amazonaws.com"
```

To enable chaos engineering via SSM, uncomment the `aws_ssm_document` block in `ssm_chaos.tf` and re-apply.

---

## What I'd improve in a production setup

- Move RDS to private subnets — currently publicly accessible for academic simplicity
- Replace hardcoded DB credentials with AWS Secrets Manager
- Add HTTPS listener on the NLB with ACM certificate
- Enable SSM chaos document for actual fault injection testing
- Add autoscaling group instead of fixed EC2 pair
- Split `docker-compose.yml` into separate frontend/backend services with health checks
