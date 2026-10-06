# Scenario 3: Microservices (webapp + dbapp) over Docker Network (No Volumes)

Divides the application into two separate microservice containers connected via a custom user-defined Docker bridge network without docker-compose or volumes.

- **`webapp`**: Serves the frontend, runs Iris ML inference, and calls `dbapp` to save/retrieve records.
- **`dbapp`**: Independent microservice that receives prediction records and saves them to SQLite.

## 🚀 How to Run

### 1. Create a Docker Network
```bash
docker network create iris-net
```

### 2. Build Both Images
```bash
docker build -t iris-dbapp:s3 ./dbapp
docker build -t iris-webapp:s3 ./webapp
```

### 3. Run the Database Microservice First
```bash
docker run -d --name dbcnt --network iris-net iris-dbapp:s3
```

### 4. Run the Webapp Microservice
Connect it to the same network and tell it where `dbapp` lives using `DB_SERVICE_URL`:
```bash
docker run -d --name webcnt --network iris-net -p 5000:5000 -e DB_SERVICE_URL=http://dbcnt:5000 iris-webapp:s3
```

### 5. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 6. Demonstration (No Volume = Data Loss on Container Removal)
If you stop and delete `dbcnt`:
```bash
docker rm -f dbcnt
docker run -d --name dbcnt --network iris-net iris-dbapp:s3
```
Any previous records are gone because no volume was mounted.

### 7. Clean Up
```bash
docker rm -f webcnt dbcnt
docker network rm iris-net
```
