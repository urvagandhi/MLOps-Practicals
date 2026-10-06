# Scenario 5: Microservices Orchestrated with Docker Compose (No Volume)

Orchestrates both `webapp` and `dbapp` using a single `docker-compose.yml` file without any volume mapping.

## 🚀 How to Run

### 1. Start Services
From within this directory (`P4/scenario_5_compose`):
```bash
docker compose up --build -d
```

### 2. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 3. Check Service Status
```bash
docker compose ps
```

### 4. Stop and Tear Down
```bash
docker compose down
```
*(Because there are no volumes attached, all stored prediction records are removed when the container is taken down).*
