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
    classDef lightBlueBox fill:#4dd0e1,stroke:#0097a7,stroke-width:2px,color:#333
    classDef greyBox fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,color:#333
    classDef darkGreenRound fill:#2e7d32,stroke:#1b5e20,stroke-width:2px,color:#fff

    subgraph DevSetup [1. DEVELOPMENT SETUP]
        direction TB
        A[Project & API<br>Setup]:::blueBox --> B[Image Handler<br>Code]:::blueBox
        B --> C[Celebrity<br>Detector Code]:::orangeBox
        C --> D[QA Engine<br>Code]:::purpleBox
        D --> E[Routes<br>Code]:::greenBox
        E --> F[Application<br>Code]:::lightBlueBox
    end
    
    subgraph Containerization [2. CONTAINERIZATION]
        direction TB
        G[Dockerfile]:::blueBox
        H[Kubernetes<br>Deployment File]:::greenBox
        G --> H
    end

    subgraph CI [3. CI / CD PIPELINE]
        direction TB
        I[Code Versioning<br>using GitHub]:::greyBox --> J[CircleCI<br>Pipeline]:::greyBox
        J --> K[Build & Push<br>Image toGAR]:::orangeBox
        K --> L[Deploy<br>to GKE]:::greenBox
    end

    M([Deployed<br>Application<br>on GKE]):::darkGreenRound

    %% Connections across subgraphs
    F --> |Triggers| G
    H -.-> |Used by| L
    L --> M

    %% Subgraph Styling
    style DevSetup fill:#fffde7,stroke:#fbc02d,stroke-dasharray: 5 5
    style Containerization fill:#e8f5e9,stroke:#4caf50,stroke-dasharray: 5 5
    style CI fill:#f3e5f5,stroke:#9c27b0,stroke-dasharray: 5 5
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
