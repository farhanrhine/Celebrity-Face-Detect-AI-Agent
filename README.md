# 🌟 Celebrity Face Detect AI Agent

A Flask web application that detects celebrity faces in uploaded images using OpenCV and identifies them using the Groq AI API. Users can also ask questions about the detected celebrity.

## What It Does

- Upload any photo
- Detects the face using OpenCV (draws a green box around it)
- Identifies the celebrity using Groq's Llama 4 AI model
- Shows info: Name, Profession, Nationality, Famous For, Top Achievements
- Ask follow-up questions about the celebrity via Q&A
- Saves Q&A history in your browser

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

## Architecture Workflow

```mermaid
graph TD
    %% Define Styles
    classDef user fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff;
    classDef ingress fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff;
    classDef k8s fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    classDef app fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff;
    classDef ext fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff;
    classDef cicd fill:#34495e,stroke:#2c3e50,stroke-width:2px,color:#fff;

    %% CI/CD Pipeline
    subgraph CI_CD["CI/CD Pipeline (CircleCI)"]
        Dev["Developer"] -->|"git push"| GitHub["GitHub Repository"]
        GitHub -->|"triggers"| CircleCI["CircleCI Pipeline"]
        CircleCI -->|"1. Build Image"| DockerBuild["Docker Build (python:3.12-slim + uv)"]
        DockerBuild -->|"2. Push Image"| GCP_AR["GCP Artifact Registry (us-central1)"]
        CircleCI -->|"3. Deploy"| GKE_Deploy["Update GKE Deployment"]
    end
    
    %% GCP Ecosystem
    subgraph GCP["Google Cloud Platform (GKE)"]
        GCP_AR -.->|"Pulls latest image"| Container
        
        %% Kubernetes Cluster
        subgraph Cluster["Kubernetes Cluster"]
            Ingress["Nginx Ingress (face-detect-ingress)"]
            CertManager["Cert-Manager (Lets Encrypt TLS)"]
            Service["K8s Service (face-detect-service)"]
            
            CertManager -.->|"Issues & Renews Certs"| Ingress
            
            subgraph Pods["Deployment: face-detect-ai-agent"]
                Container["Flask App Container<br>(app.py : Port 5000)<br>+ OpenCV Face Detection"]
            end
            
            Ingress -->|"Routes HTTP/S Traffic"| Service
            Service -->|"Load Balances"| Container
        end
    end

    %% External & Users
    User["End User<br>(Web Browser)"] -->|"HTTPS (face-detect-ai.tech)"| Ingress
    
    GroqAPI["Groq API<br>(Llama 4 Maverick)"]
    Container -->|"API Calls (Identity + Q&A)"| GroqAPI

    %% Assign Styles
    class Dev,User user;
    class Ingress,Service ingress;
    class Container,Pods app;
    class GroqAPI ext;
    class GitHub,CircleCI,DockerBuild,GCP_AR,GKE_Deploy cicd;
    class CertManager k8s;
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
