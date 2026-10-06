# MLOps Practical 4: Docker & Microservice Scenarios

All **8 Docker Practical Scenarios** are organized into dedicated, self-contained directories inside `P4`. Every scenario uses the clean, unified **Iris classification frontend** from P4 without any unnecessary complexity.

---

## 📁 Scenarios Overview

| # | Scenario | Directory / File | Description |
|:---:|:---|:---|:---|
| **1** | **Dockerize Webapp** | [`scenario_1_dockerize_webapp/`](./scenario_1_dockerize_webapp) | Single container running Flask webapp + ML inference |
| **2** | **Dockerize Webapp with DB** | [`scenario_2_dockerize_webapp_db/`](./scenario_2_dockerize_webapp_db) | Monolith container with Flask webapp + internal SQLite DB |
| **3** | **Webapp + DBapp (Network)** | [`scenario_3_microservices_network/`](./scenario_3_microservices_network) | 2 containers communicating over Docker bridge network (no volume) |
| **4** | **Webapp + DBapp with Volume** | [`scenario_4_microservices_volume/`](./scenario_4_microservices_volume) | 2 containers on Docker network with persistent Docker volume |
| **5** | **Compose (No Volume)** | [`scenario_5_compose/`](./scenario_5_compose) | Orchestrated using `docker-compose.yml` (no volume) |
| **6** | **Compose with Volume** | [`scenario_6_compose_volume/`](./scenario_6_compose_volume) | Orchestrated using `docker-compose.yml` with named volume |
| **7** | **Export/Import + Save/Load** | [`scenario_7_commands.md`](./scenario_7_commands.md) | Command reference and cheat sheet |
| **8** | **Multi-stage Build** | [`scenario_8_multistage_build/`](./scenario_8_multistage_build) | Dockerfile with multi-stage build (builder → slim runtime) |

---

## ⚡ Quick-Start Commands

### Scenario 1: Dockerize Webapp
```bash
cd scenario_1_dockerize_webapp
docker build -t iris-webapp:s1 .
docker run -d -p 5000:5000 --name iris-web-s1 iris-webapp:s1
# Access: http://localhost:5000
docker stop iris-web-s1 && docker rm iris-web-s1
```

### Scenario 2: Dockerize Webapp with DB
```bash
cd scenario_2_dockerize_webapp_db
docker build -t iris-webapp-db:s2 .
docker run -d -p 5000:5000 --name iris-web-db-s2 iris-webapp-db:s2
# Access: http://localhost:5000 & http://localhost:5000/records
docker stop iris-web-db-s2 && docker rm iris-web-db-s2
```

### Scenario 3: Microservices over Docker Network (No Volumes)
```bash
cd scenario_3_microservices_network
docker network create iris-net
docker build -t iris-dbapp:s3 ./dbapp
docker build -t iris-webapp:s3 ./webapp
docker run -d --name dbcnt --network iris-net iris-dbapp:s3
docker run -d --name webcnt --network iris-net -p 5000:5000 -e DB_SERVICE_URL=http://dbcnt:5000 iris-webapp:s3
# Access: http://localhost:5000 & http://localhost:5000/records
docker rm -f webcnt dbcnt
docker network rm iris-net
```

### Scenario 4: Microservices with Docker Volume (No Compose)
```bash
cd scenario_4_microservices_volume
docker network create iris-net
docker volume create iris-db-vol
docker build -t iris-dbapp:s4 ./dbapp
docker build -t iris-webapp:s4 ./webapp
docker run -d --name dbcnt --network iris-net -v iris-db-vol:/app/data iris-dbapp:s4
docker run -d --name webcnt --network iris-net -p 5000:5000 -e DB_SERVICE_URL=http://dbcnt:5000 iris-webapp:s4
# Access: http://localhost:5000 & http://localhost:5000/records
# Test persistence by removing and re-running dbcnt with the same volume!
docker rm -f webcnt dbcnt
docker network rm iris-net
docker volume rm iris-db-vol
```

### Scenario 5: Docker Compose (No Volume)
```bash
cd scenario_5_compose
docker compose up --build -d
# Access: http://localhost:5000 & http://localhost:5000/records
docker compose down
```

### Scenario 6: Docker Compose with Volume
```bash
cd scenario_6_compose_volume
docker compose up --build -d
# Access: http://localhost:5000 & http://localhost:5000/records
docker compose down      # Containers removed, data volume is preserved!
docker compose down -v   # Removes containers AND the named volume
```

### Scenario 7: Export/Import + Load/Save
Refer to [`scenario_7_commands.md`](./scenario_7_commands.md) for full explanations and comparison.

### Scenario 8: Multi-Stage Build
```bash
cd scenario_8_multistage_build
docker compose up --build -d
# Access: http://localhost:5000 & http://localhost:5000/records
# Or build standalone webapp image:
docker build -t iris-webapp:multistage ./webapp
docker compose down
```
