# Cloud AI Personal Productivity Router

## Summary

Cloud AI Personal Productivity Router is a serverless, cloud-native API that transforms user goals (e.g., “prepare for AWS certification” or “improve piano sight-reading”) into structured, actionable learning plans using large language models.

This project demonstrates production-aware AI system design, including:
- LLM orchestration (intent classification + structured generation)
- Cost-aware AI integration
- Usage logging & observability
- Serverless architecture (AWS Lambda)
- Infrastructure as Code (Terraform)
- CI/CD automation

Check out the live demo here: [Live Demo](https://leejamie-42.github.io/goal-router/)



## Quick Start

### Prerequisites
- Python 3.11+
- AWS Account (for deployment)
- Docker (optional, for local development)

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/goal-router.git
cd goal-router

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows (PowerShell)
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set environment variables
# Create .env file or export:
export USE_MOCK_AWS=true
export AWS_REGION=ap-southeast-2

# 6. Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Then visit:** http://localhost:8000/docs

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up

# Or manually:
docker build -t ai-router .
docker run -p 8000:8000 -e USE_MOCK_AWS=true ai-router
```


## Example Usage

### Making a Request

```bash
curl -X POST "http://localhost:8000/api/v1/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Prepare for AWS Solutions Architect certification",
    "context": "Beginner with basic cloud knowledge"
  }'
```

### Response

```json
{
  "request_id": "abc-123-def",
  "goal": "Prepare for AWS Solutions Architect certification",
  "category": "certification",
  "estimated_duration_weeks": 12,
  "weekly_breakdown": [
    {
      "week_number": 1,
      "focus_area": "AWS Fundamentals",
      "tasks": [
        "Complete AWS Cloud Practitioner Essentials course",
        "Set up AWS Free Tier account",
        "Practice with IAM users and policies"
      ],
      "milestone": "Understand core AWS services and concepts"
    }
    // ... more weeks
  ],
  "resources": [
    {
      "title": "AWS Solutions Architect Study Guide",
      "url": "https://example.com/guide",
      "resource_type": "documentation"
    }
  ],
  "total_estimated_hours": 96.0,
  "created_at": "2026-02-10T10:30:00Z"
}
```




## Architecture

### High-Level Design

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     ▼
┌─────────────────┐
│  API Gateway    │ ← HTTP API (modern, cost-effective)
│  (HTTP API)     │
└────┬────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│         Lambda (FastAPI)             │
│  ┌────────────────────────────────┐  │
│  │   1. Intent Classifier         │  │ ← Categorizes request
│  │   2. Cost Guardrails           │  │ ← Enforces token limits
│  │   3. Plan Generator            │  │ ← Creates structured plan
│  │   4. Metrics Publisher         │  │ ← CloudWatch metrics
│  │   5. Structured Logger         │  │ ← JSON logs
│  └────────────────────────────────┘  │
└──────┬───────────────────────────────┘
       │
       ├──────────────► DynamoDB (Usage Logs)
       │
       ├──────────────► CloudWatch (Metrics & Logs)
       │
       └──────────────► Bedrock (Claude 3)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **API Gateway** | HTTP endpoint, request routing |
| **Lambda** | Serverless compute, runs FastAPI |
| **Amazon Bedrock** | Managed LLM service (Claude 3) |
| **DynamoDB** | Usage logs, cost tracking |
| **CloudWatch** | Metrics, logs, monitoring |


## Technology Stack

### Backend
- **Python 3.12** - Modern, type-safe Python
- **FastAPI** - High-performance web framework
- **Mangum** - ASGI adapter for AWS Lambda
- **Pydantic v2** - Data validation and serialization

### Cloud & Infrastructure
- **AWS Lambda** - Serverless compute
- **API Gateway** (HTTP API) - Modern API routing
- **Amazon Bedrock** - Managed LLM service
- **DynamoDB** - NoSQL database for logs
- **CloudWatch** - Observability platform

### DevOps
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD automation
- **Docker** - Containerization for local dev
- **Pre-commit** - Code quality hooks


## Project Structure

```
goal-router/
├── app/                        # Application code
│   ├── main.py                # FastAPI application entry
│   ├── router.py              # API endpoints
│   ├── config.py              # Configuration management
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   └── services/
│       ├── classifier.py      # Intent classification
│       ├── planner.py         # Plan generation
│       ├── cost_guard.py      # Token limit enforcement
│       ├── db_logger.py       # DynamoDB logging
│       ├── logger.py          # Structured logging
│       └── metrics.py         # CloudWatch metrics
├── terraform/                 # Infrastructure as Code
│   ├── main.tf
│   ├── lambda.tf
│   ├── api_gateway.tf
│   ├── dynamodb.tf
│   ├── iam.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── cloudwatch_dashboard.tf
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Local dev environment
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Dev dependencies
└── README.md
```


## Key Features

### 1. Multi-Step LLM Orchestration
Not just a prompt wrapper—implements intelligent routing:
- **Intent Classification** - Categorizes goals before generation
- **Structured Output** - Enforces JSON schema for reliability
- **Context Enrichment** - Tailors prompts based on category

### 2. Cost Control & Guardrails
Production-aware AI integration:
- **Token Estimation** - Prevents expensive requests
- **Maximum Input Limits** - Configurable thresholds
- **Request Rejection** - Fails fast on over-budget requests
- **Usage Tracking** - DynamoDB logs for cost analysis

### 3. Production Observability
Enterprise-grade monitoring:
- **Structured JSON Logs** - Queryable in CloudWatch Logs Insights
- **Custom Metrics** - Token usage, latency, success rates
- **Request Tracing** - Unique IDs for distributed tracing
- **CloudWatch Dashboard** - Visual monitoring at a glance

### 4. Serverless Architecture
Cloud-native design:
- **Auto-scaling** - Handles 0 to 10,000+ requests
- **Pay-per-use** - No idle server costs
- **Managed Services** - DynamoDB, Bedrock, CloudWatch
- **High Availability** - Multi-AZ by default

### 5. Infrastructure as Code
Reproducible deployments:
- **Terraform** - All infrastructure defined in code
- **Version Controlled** - Infrastructure changes tracked in Git
- **Environment Separation** - Dev/staging/prod configurations
- **One-Command Deployment** - `terraform apply`



## Security Considerations

- **Input Validation** - Pydantic enforces strict schemas
- **Token Limits** - Prevents runaway costs and abuse
- **IAM Least Privilege** - Lambda has minimal required permissions
- **No Hardcoded Secrets** - Environment variables for config
- **Dependency Scanning** - Automated security scans in CI
- **Secret Detection** - Trufflehog prevents credential leaks



## Design Decisions

### Why Serverless?
- **Cost Efficiency** - Only pay for actual requests
- **Operational Simplicity** - No server management
- **Auto-Scaling** - Handles traffic spikes automatically

### Why Multi-Step Orchestration?
A simple prompt wrapper would just pass the goal directly to the LLM. This project implements:
1. **Classification** - Determines goal type (certification, skill, fitness, etc.)
2. **Context Enrichment** - Adjusts system prompt based on category
3. **Structured Generation** - Enforces JSON schema
4. **Post-Processing** - Validates and enhances output

This produces more reliable, structured results.

### Why DynamoDB for Logs?
- **Serverless** - No database servers to manage
- **Fast Writes** - Single-digit millisecond latency
- **Flexible Schema** - Easy to add new log fields
- **Cost-Effective** - Pay only for what you use

### Why CloudWatch Metrics?
- **Native AWS Integration** - Works seamlessly with Lambda
- **Dashboards** - Visual monitoring
- **Alarms** - Automated alerting
- **Long Retention** - 15 months of data


## Performance & Cost

### Typical Request Profile
- **Latency**: 1-3 seconds (classification + generation)
- **Token Usage**: 500-2000 tokens per request
- **Cost**: ~$0.002-0.01 per request (Bedrock pricing)

### Scalability
- **Concurrent Requests**: 1000+ (Lambda default)
- **Max Throughput**: 10,000+ requests/minute (with quota increase)
- **Cold Start**: ~1-2 seconds (FastAPI + Mangum)



## Deployment

### Prerequisites
- AWS Account
- Terraform installed
- AWS CLI configured

### Deploy to AWS

```bash
# 1. Navigate to Terraform directory
cd terraform

# 2. Initialize Terraform
terraform init

# 3. Review planned changes
terraform plan

# 4. Deploy infrastructure
terraform apply

# 5. Get API endpoint
terraform output api_endpoint

### Environment Variables

Set these in AWS Lambda:

```bash
USE_MOCK_AWS=false
AWS_REGION=ap-southeast-2
APP_AWS_REGION=ap-southeast-2
BEDROCK_REGION=us-east-1
DYNAMODB_TABLE_NAME=ai-router-usage-logs
```



## Monitoring

### CloudWatch Logs Insights Queries

**Average Latency by Category:**
```sql
fields @timestamp, request_id, category, latency_ms
| filter event_type = "llm_call"
| stats avg(latency_ms) as avg_latency by category
| sort avg_latency desc
```

**Token Usage by Hour:**
```sql
fields @timestamp, total_tokens
| filter event_type = "llm_call"
| stats sum(total_tokens) as tokens by bin(1h)
```

**Error Rate:**
```sql
fields @timestamp
| filter event_type = "error"
| stats count() as error_count by bin(5m)
```

### CloudWatch Dashboard

After deployment, view the dashboard:
```
AWS Console → CloudWatch → Dashboards → ai-router-dashboard-dev
```

Shows:
- Request count by status (success/failure)
- Response latency (p50, p95, p99)
- Token usage trends
- Cost guard triggers
- Requests by category



## Future Enhancements
- Authentication layer (JWT / Cognito)
- Support multiple LLM models (GPT-4, etc.)
- Implement rate limitng per user
- Redis caching
- Plan persistence

## Technical Challenges
**Challenge**: Lambda Timeouts with large LLM responses, causing execution failures.
**Solution**: Increased Lambda timeout to 300 seconds; Added frontend loading state to handle longer inference times

**Challenge**: Bedrock rate limits during development
**Solution**: Implemented mock mode (`USE_MOCK_AWS=true`) for local testing without hitting APIs

**Challenge**: Native Python dependencies in AWS Lambda - pydantic_core failed to import in lambda due to architecture mismatch and OS-level binary compilation differences.
**Solution**: Built deployment package inside the official Lambda Docker runtime; Explicitly matched Lambda architecture; Pinned dependency versions in requirements.txt

**Challenge**: Lambda cold starts affecting latency
**Solution**: Accepted as trade-off for cost savings; could add provisioned concurrency for production

## Lessons Learned
1. **Native Dependencies Matter in Serverless**: Python libraries with compiled extensions (like Pydantic v2) require architecture-aware builds. Dockerized packaging is essential.
2. **AI Latency Is Non-Deterministic**: LLM inference time varies with token count. Serverless timeouts must account for worst-case responses.
3. **Observability Is Not Optional**: Structured logs, request IDs, and token metrics made debugging Lambda and API Gateway issues tractable.
4. **Cost Guardrails Should Be Built Early**: Token usage tracking prevented accidental cost spikes during experimentation.
5. **Infrastructure as Code Enables Confidence**: Being able to terraform destroy and terraform apply the entire stack reduced fear of breaking changes.


## License
MIT License

## Author
Built by Jamie Lee as a portfolio project to demonstrate cloud-native AI system design and production engineering practices.
