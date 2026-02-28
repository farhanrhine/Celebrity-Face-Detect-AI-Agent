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
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#dbeafe', 'primaryTextColor': '#1e3a5f', 'primaryBorderColor': '#2563eb', 'lineColor': '#3b82f6', 'secondaryColor': '#f0fdf4', 'tertiaryColor': '#fef3c7', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart TD
    classDef phase1 fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
    classDef phase2 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#92400e
    classDef phase3 fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#166534
    classDef live fill:#fce7f3,stroke:#ec4899,stroke-width:2px,color:#9d174d

    subgraph Phase1 [1. LOCAL DEV & CONFIG]
        direction LR
        A(["💻 Flask App<br>Source Code"]):::phase1 --> B["📦 Create<br>Dockerfile"]:::phase1
        B --> C["🚀 Kubernetes<br>Deployment.yaml"]:::phase1
    end

    subgraph Phase2 [2. CI/CD PIPELINE]
        direction LR
        D["📤 Pipeline via<br>GitHub"]:::phase2 --> E["🏗️ Build Image<br>on GCP"]:::phase2
        E --> F["🗄️ Push to<br>Gar"]:::phase2
        F --> G["☸️ Deploy to<br>GKE Cluster"]:::phase2
    end

    subgraph Phase3 [3. DOMAIN & HTTPS SETUP]
        direction LR
        H["🌐 Register<br>.TECH Domain"]:::phase3 --> I["🗺️ Map DNS to<br>GKE IP"]:::phase3
        I --> J["🚦 Install<br>NGINX Ingress"]:::phase3
        J --> K["🔒 Setup Let's<br>Encrypt"]:::phase3
        K --> L["📑 Apply<br>ingress.yaml"]:::phase3
    end

    M{"🎉 Live App on<br>Custom Domain"}:::live

    %% Connections across subgraphs
    C -->|"Commit & Push"| D
    G -->|"Use Raw IP"| H
    L -->|"Traffic Secured"| M

    %% Subgraph Styling
    style Phase1 fill:#ffffff,stroke:#2563eb,stroke-dasharray: 5 5,stroke-width:2px,color:#1e40af
    style Phase2 fill:#ffffff,stroke:#f59e0b,stroke-dasharray: 5 5,stroke-width:2px,color:#92400e
    style Phase3 fill:#ffffff,stroke:#22c55e,stroke-dasharray: 5 5,stroke-width:2px,color:#166534
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
