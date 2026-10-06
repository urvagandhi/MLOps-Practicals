# Scenario 4: Microservices (webapp + dbapp) with Volume (No Docker Compose)

Runs the microservices architecture on a user-defined network using a named Docker Volume (`iris-db-vol`) mounted to `/app/data` in the `dbapp` container to ensure data persistence across container restarts or deletions.

## 🚀 How to Run

### 1. Create Network and Volume
```bash
docker network create iris-net
docker volume create iris-db-vol
```

### 2. Build Both Images
```bash
docker build -t iris-dbapp:s4 ./dbapp
docker build -t iris-webapp:s4 ./webapp
```

### 3. Run the Database Microservice with the Volume
```bash
docker run -d --name dbcnt --network iris-net -v iris-db-vol:/app/data iris-dbapp:s4
```

### 4. Run the Webapp Microservice
```bash
docker run -d --name webcnt --network iris-net -p 5000:5000 -e DB_SERVICE_URL=http://dbcnt:5000 iris-webapp:s4
```

### 5. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 6. 🧪 Test Persistence (Proof of Volume Working)
1. Predict 1 or 2 species at http://localhost:5000 and confirm they show up on http://localhost:5000/records.
2. Forcefully remove the database container:
   ```bash
   docker rm -f dbcnt
   ```
3. Start a new database container with the same volume:
   ```bash
   docker run -d --name dbcnt --network iris-net -v iris-db-vol:/app/data iris-dbapp:s4
   ```
4. Refresh http://localhost:5000/records — all your previous predictions are **STILL THERE!**

### 7. Clean Up
```bash
docker rm -f webcnt dbcnt
docker network rm iris-net
docker volume rm iris-db-vol
```
