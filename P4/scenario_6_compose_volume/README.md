# Scenario 6: Microservices with Docker Compose + Persistent Volume

Orchestrates both `webapp` and `dbapp` using `docker-compose.yml` with a named Docker Volume (`iris_db_data`) mounted to the database container to persist predictions across container tear-downs.

## 🚀 How to Run

### 1. Start Services
From within this directory (`P4/scenario_6_compose_volume`):
```bash
docker compose up --build -d
```

### 2. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 3. 🧪 Test Volume Persistence
1. Add a prediction at http://localhost:5000.
2. Stop and take down the containers:
   ```bash
   docker compose down
   ```
3. Start the containers again:
   ```bash
   docker compose up -d
   ```
4. Refresh http://localhost:5000/records — the database records are **persisted**!

### 4. Complete Tear Down (Including Volume Removal)
```bash
docker compose down -v
```
*(The `-v` flag removes the named volume when you are completely finished).*
