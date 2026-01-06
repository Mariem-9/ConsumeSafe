# Project: ConsumeSafe Application

## Objective:
Build an application to help users make safer consumption choices by checking if products are on a boycott list.
## Key Features:
    * Product Check: User inputs a product, app checks if it’s on a boycott list.
    * Suggestions: If the product is boycotted, highlight it and suggest alternative Tunisian products.
## Tech Stack:
    * Backend: Python (for APIs and logic)
    * Version Control: Git
    * CI/CD: Any Continuous Integration server of your choice (e.g., GitHub Actions, GitLab CI, Jenkins)
    * Containerization: Docker image for deployment
    * Orchestration: Kubernetes (k8s) cluster deployment
    * Security: Harden the application and infrastructure
    * AI Integration: Optional; can be used to improve product recommendations or automate boycott list updates
## Deliverables:
    * Working application deployed in Kubernetes
    * Dockerized microservices (if applicable)
    * Secure pipelines and deployment
    * Optional AI features for smarter recommendations

### Step 1: Backend + Core Functionality : Have a working API to check boycott products and suggest alternatives.
1. Create the Github repository named ConsumeSafe then Clone it on PC
```
cd C:\Users\user\Documents\15 H\DevSecOps
git clone https://github.com/Mariem-9/ConsumeSafe.git
cd ConsumeSafe
```
2. Create Python Virtual Environment
```
python -m venv venv                     # Isolates project dependencies
venv\Scripts\activate                   # Activate it
```
3. Install backend dependencies
```
pip install fastapi uvicorn pandas      # For FastAPI (modern, fast, perfect for DevOps & k8s)
pip freeze > requirements.txt           # Saved in requirements.txt 
```
4. Create boycott_list.csv with 100 products and mixed statuses (Boycott / Ok) and Tunisian alternatives where needed.
5. Create FastAPI backend (app.py)

#### Project structure
```
ConsumeSafe/
│
├── app.py
├── boycott_list.csv
├── requirements.txt
└── venv/
```

> Python backend running locally, checking products against boycott list. 