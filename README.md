# 🌟 Celebrity Face Detect AI Agent

A Flask web application that detects celebrity faces in uploaded images using OpenCV and identifies them using the Groq AI API. Users can also ask questions about the detected celebrity.

## What It Does

- Upload any photo
- Detects the face using OpenCV (draws a green box around it)
- Identifies the celebrity using Groq's Llama 4 AI model
- Shows info: Name, Profession, Nationality, Famous For, Top Achievements
- Ask follow-up questions about the celebrity via Q&A
- Saves Q&A history in your browser

## Workflow

```mermaid
flowchart LR
    %% Define Styles
    classDef blueBox fill:#1976d2,stroke:#0d47a1,stroke-width:2px,color:#fff
    classDef greenBox fill:#388e3c,stroke:#1b5e20,stroke-width:2px,color:#fff
    classDef orangeBox fill:#f57c00,stroke:#e65100,stroke-width:2px,color:#fff
    classDef purpleBox fill:#7b1fa2,stroke:#4a148c,stroke-width:2px,color:#fff
    classDef darkGreenRound fill:#2e7d32,stroke:#1b5e20,stroke-width:2px,color:#fff
    classDef tealBox fill:#00796b,stroke:#004d40,stroke-width:2px,color:#fff
    classDef greyBox fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,color:#333

    subgraph Phase1 [1. LOCAL DEV & CONFIG]
        direction TB
        App[Flask App<br>Source Code]:::blueBox
        Docker[Dockerfile]:::orangeBox
        K8s[Kubernetes<br>Deployment.yaml]:::greenBox
        App --> Docker
        Docker --> K8s
    end

    subgraph Phase2 [2. CI/CD PIPELINE]
        direction TB
        Git[Push Code<br>to GitHub]:::greyBox
        Circle[CircleCI<br>Workflow]:::greyBox
        Build[Build Docker<br>Image on GCP]:::blueBox
        GAR[Push to GCP<br>Artifact Registry]:::orangeBox
        GKE[Deploy App<br>to GKE Cluster]:::greenBox

        Git --> Circle
        Circle --> Build
        Build --> GAR
        GAR --> GKE
    end

    subgraph Phase3 [3. DOMAIN & HTTPS SETUP]
        direction TB
        Domain[Register .TECH<br>Domain]:::purpleBox
        DNS[Map DNS Record<br>to GKE IP]:::purpleBox
        Nginx[Install NGINX<br>Ingress]:::tealBox
        Cert[Setup Let's Encrypt<br>Cert-Manager]:::tealBox
        Ingress[Apply ingress.yaml<br>& ClusterIssuer]:::tealBox

        Domain --> DNS
        DNS --> Nginx
        Nginx --> Cert
        Cert --> Ingress
    end

    Live([Live App on<br>Custom Domain]):::darkGreenRound

    %% Connections across subgraphs
    K8s --> |Commit to| Git
    GKE --> |Raw IP used by| Domain
    Ingress --> |Routes Traffic to| Live

    %% Subgraph Styling
    style Phase1 fill:#fffde7,stroke:#fbc02d,stroke-dasharray: 5 5
    style Phase2 fill:#f3e5f5,stroke:#9c27b0,stroke-dasharray: 5 5
    style Phase3 fill:#e0f7fa,stroke:#00acc1,stroke-dasharray: 5 5
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Face Detection | OpenCV (Haar Cascade) |
| AI / LLM | Groq API (Llama 4 Maverick) |
| Package Manager | uv |
| Containerization | Docker |
| Orchestration | Kubernetes (GKE) |
| CI/CD | CircleCI |
| Cloud | Google Cloud Platform (GCP) |

## Project Structure

```
face-detect-ai-agent/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # URL routes and request handling
│   └── utils/
│       ├── celebrity_detector.py   # Groq API — identifies celebrity
│       ├── image_handler.py        # OpenCV — detects face in image
│       └── qa_engine.py            # Groq API — answers questions
├── templates/
│   └── index.html           # Frontend UI
├── static/
│   └── style.css            # Styling
├── app.py                   # Entry point
├── Dockerfile               # Docker build config
├── kubernetes-deployment.yaml  # K8s deployment + service
├── pyproject.toml           # Project dependencies
└── .circleci/
    └── config.yml           # CI/CD pipeline
```

## Run Locally

**1. Clone the repo:**

```bash
git clone https://github.com/farhanrhine/face-detect-ai-agent-gcp.git
cd face-detect-ai-agent-gcp
```

**2. Create a `.env` file:**

```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
```

**3. Install dependencies and run:**

```bash
uv sync
uv run app.py
```

**4. Open your browser:** `http://localhost:5000`

## Run with Docker

```bash
docker build -t face-detect-ai-agent .
docker run -p 5000:5000 --env-file .env face-detect-ai-agent
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) |
| `SECRET_KEY` | Flask secret key (any random string) |

## Deployment

This project is deployed on **Google Kubernetes Engine (GKE)** with an automated **CircleCI** pipeline.

Every `git push` to `main` automatically:

1. Builds a Docker image
2. Pushes it to GCP Artifact Registry
3. Deploys to GKE

**CircleCI Environment Variables required:**

- `GCLOUD_SERVICE_KEY` — Base64-encoded GCP service account key
- `GOOGLE_PROJECT_ID` — Your GCP project ID
- `GKE_CLUSTER` — Your GKE cluster name
- `GOOGLE_COMPUTE_REGION` — GCP region (e.g. `us-central1`)
