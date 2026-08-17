# Multimodal Fake News & Misinformation Detector

> **Project Delivery Repository | AI/ML + Full-Stack Application**

A production-oriented prototype for detecting potentially misleading content through **joint text and image analysis**, with explainable evidence, human review feedback, analytics, and a browser-extension integration.

## Project Status

**Delivery:** MVP / Academic-Industry Project Delivery  
**Version:** 0.1.0  
**Primary Branch:** `main`  
**Owner:** PANKAJ955956

## Key Capabilities

- Text-only claim analysis
- Image-only visual analysis
- Multimodal text + image analysis
- Public article URL analysis
- Confidence-based prediction and review thresholds
- Explainability/evidence panels
- Human fact-checker feedback workflow
- Prediction history and analytics
- PostgreSQL persistence
- Redis caching
- React + TypeScript frontend
- FastAPI backend
- Docker / Docker Compose deployment
- Browser extension prototype
- Automated backend tests

## Architecture

```text
Client → React Frontend → FastAPI API → Preprocessing
                                     ↙          ↘
                              Text/Vision       Services
                                  ↓                ↓
                              Fusion/Classifier → Explainability
                                  ↓                ↓
                              Confidence → PostgreSQL / Redis
```

## Repository Structure

```text
.
├── api/                    # API documentation
├── backend/                # FastAPI backend, ML services, tests
├── browser-extension/      # Browser extension prototype
├── database/               # Database initialization scripts
├── datasets/               # Dataset documentation and demo data
├── docs/                   # Project delivery and engineering documents
├── frontend/               # React + TypeScript frontend
├── .env.example            # Safe configuration template
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI, Uvicorn |
| ML/NLP | Transformers-compatible architecture, RoBERTa/BART configuration |
| Vision | CLIP configuration |
| Database | PostgreSQL, SQLAlchemy |
| Cache | Redis |
| Testing | Pytest |
| API Docs | OpenAPI / Swagger |
| Deployment | Docker, Docker Compose |
| Extension | HTML, CSS, JavaScript |

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker compose up --build
```

## API Surface

The backend exposes endpoints for health checks, text/image/multimodal/URL analysis, human feedback, prediction history, analytics, and model information. See [`api/README.md`](api/README.md).

## Testing

```bash
cd backend
pytest -q
```

## Delivery Documentation

The `docs/` directory contains the engineering and delivery artifacts expected for a professional project handover: project scope, high-level design, low-level design, API contract, deployment runbook, QA criteria, security/responsible-AI guidance, and handover checklist.

## Responsible AI

This system is intended as a **decision-support and screening tool**, not as an unquestionable source of truth. Predictions should be reviewed with source evidence and human judgment, particularly for high-impact claims.

## Security

Never commit production credentials or `.env` files. Uploaded media should be treated as untrusted input. Production deployments should use HTTPS, restricted CORS, authentication/authorization, rate limiting, secure secret storage, and controlled media retention.

## License

See [`LICENSE`](LICENSE).
