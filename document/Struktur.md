En välorganiserad kodstruktur underlättar för utveckling, underhåll och samarbete när projektet ligger i ett GitHub-repo. Här är en rekommenderad struktur för ditt FastAPI-projekt:

graphql
￼Copy code
fastapi-kubernetes-app/
├── app/
│ ├── **init**.py # Gör 'app' till ett Python-paket
│ ├── main.py # Huvudfilen för FastAPI-applikationen
│ ├── models.py # SQLAlchemy-modeller
│ ├── database.py # Databasinställningar och session
│ ├── schemas.py # Pydantic-scheman (validering)
│ ├── crud.py # CRUD-operationer (hantering av databasen)
│ └── routers/ # Mappar för olika API-routers
│ ├── **init**.py
│ ├── items.py # Routes för att hantera `items`
│ └── users.py # Exempel på ytterligare route
├── config/
│ ├── settings.py # Hantering av miljövariabler och konfigurationer
│ ├── logging_config.yaml # Konfigurationsfil för logging (valfritt)
├── tests/
│ ├── **init**.py
│ ├── test_main.py # Enhetstester för API:n
│ └── test_database.py # Tester för databasen
├── kubernetes/
│ ├── postgres.yaml # Kubernetes-manifest för PostgreSQL
│ ├── fastapi.yaml # Kubernetes-manifest för FastAPI
│ └── secrets.yaml # Eventuella Kubernetes-hemligheter
├── .github/
│ ├── workflows/
│ └── ci-cd.yaml # GitHub Actions-fil för CI/CD-pipelines
├── .dockerignore # Ignorera onödiga filer vid Docker-build
├── .gitignore # Ignorera filer i Git-repot
├── Dockerfile # Dockerfil för att bygga applikationen
├── requirements.txt # Python-dependenser
├── README.md # Dokumentation för projektet
└── LICENSE # Licensfil (valfritt)
Beskrivning av mappar och filer

1. app/
   Här ligger själva applikationen:

main.py: Huvudfilen som startar FastAPI.
models.py: SQLAlchemy-modeller för databasen.
database.py: Skapar databaskoppling och hanterar transaktioner.
schemas.py: Definierar Pydantic-scheman för dataöverföring.
crud.py: Centraliserar CRUD-operationer för att hålla koden ren.
routers/: Delar upp API-endpoints i olika filer för bättre organisation. 2. config/
Hanterar inställningar och konfiguration:

settings.py: Centraliserar miljövariabler och standardkonfigurationer.
logging_config.yaml (valfritt): Konfigurerar avancerad logging. 3. tests/
Enhetstester och integrationstester för att säkerställa kvalitet.
Använd pytest för testning och inkludera tester för alla endpoints och databasoperationer. 4. kubernetes/
Alla Kubernetes-manifest samlade här. Lätt att underhålla:
postgres.yaml: Databasen.
fastapi.yaml: Applikationen.
secrets.yaml: Hantering av hemligheter (t.ex., databasanvändare och lösenord).

5. Övriga filer
   .gitignore: Ignorera onödiga filer som **pycache**, .env, \*.pyc, osv.
   .dockerignore: Exkludera filer från Docker-build (som tests/ eller .git/).
   README.md: Beskriv projektet, dess syfte, och hur det används.

## CI/CD med GitHub Actions

Konfigurera GitHub Actions för CI/CD i .github/workflows/ci-cd.yaml. Exempel på en pipeline:

yaml
￼Copy code
name: CI/CD Pipeline

on:
push:
branches: - main

jobs:
build:
runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest tests/

    - name: Build Docker image
      run: docker build -t your-dockerhub-username/fastapi-app:latest .

    - name: Push Docker image
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
      run: docker push your-dockerhub-username/fastapi-app:latest
