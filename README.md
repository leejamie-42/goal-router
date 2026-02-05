# Cloud AI Personal Productivity Router

## To run the application
```bash
# 1. Clone repository
git clone https://github.com/yourusername/cloud-ai-productivity-router.git

# 2. Navigate into project
cd cloud-ai-productivity-router

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment

# Windows (PowerShell)
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run locally
uvicorn app.main:app --reload

```
## Then visit:
```bash
http://127.0.0.1:8000/docs
```



## Summary

Cloud AI Personal Productivity Router is a serverless, cloud-native API that transforms user goals (e.g., “prepare for AWS certification” or “improve piano sight-reading”) into structured, actionable learning plans using large language models.

This project demonstrates production-aware AI system design, including:
- LLM orchestration (intent classification + structured generation)
- Cost-aware AI integration
- Usage logging & observability
- Serverless architecture (AWS Lambda)
- Infrastructure as Code (Terraform)
- CI/CD automation

## Why This Project Matters

This project showcases:
- Real-world AWS architecture (Lambda + API Gateway + DynamoDB)
- AI integration beyond simple prompt wrappers
- Cost control and token guardrails
- Observability via CloudWatch metrics & logs
- Clean API design using FastAPI
- Infrastructure provisioning with Terraform
- Production deployment mindset

## Key Features

### Goal-Based Plan Generation
- Accepts high-level user goals
- Classifies intent before generation
- Produces structured weekly action plans
- Returns measurable milestones

### LLM Orchestration
- Intent classification layer
- Structured JSON output enforcement
- Multi-step reasoning pipeline

### Cost Guardrails
- Token estimation
- Maximum input length validation
- Budget-aware request rejection

### Usage Logging
- Logs request metadata
- Tracks token usage
- Records latency metrics
- Stores structured usage logs in DynamoDB

### Observability
- Structured JSON logging
- CloudWatch metrics tracking
- Request-level tracing

## Architecture

### High-Level Architecture
Client → API Gateway → AWS Lambda (FastAPI)
                    ↓
                Amazon Bedrock (LLM)
                    ↓
                DynamoDB (Usage Logs)
                    ↓
                CloudWatch (Logs + Metrics)

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- Mangum (Lambda adapter)
- Pydantic

### Cloud
- AWS Lambda
- API Gateway (HTTP API)
- Amazon Bedrock
- DynamoDB
- CloudWatch

### Infrastructure
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)
- Docker (Local development)

## Project Structure
cloud-ai-productivity-router/
├── app/
│   ├── main.py
│   ├── router.py
│   ├── services/
│   ├── models/
├── terraform/
├── tests/
├── .github/workflows/
├── Dockerfile
├── requirements.txt
└── README.md

## Security Considerations
- Input validation via Pydantic
- Token length guardrails
- IAM least-privilege policies
- No hardcoded secrets
- Environment variable configuration

## Design Decisions

### Serverless Architecture
Chosen for:
- Scalability
- Cost efficiency
- Operational simplicity

### Structured LLM Output
Plans are returned in strict JSON schema format to:
- Ensure reliability
- Support future frontend integration
- Prevent hallucinated free-text responses

### Usage Logging
Each request logs:
- Goal length
- Token usage
- Latency
- Classification category

This ensures cost monitoring and production readiness.

## Future Enhancements
- Authentication layer (JWT / Cognito)
- Rate limiting
- Multi-model routing
- Budget caps per user
- Redis caching
- Frontend dashboard
- Plan persistence

## Challenges & Solutions
(To be added later.)

## Lessons Learned
(To be added later.)

## License
MIT License

## Author
Built by Jamie Lee as a portfolio project to demonstrate cloud-native AI system design and production engineering practices.
