# Scenario 2: Dockerize Webapp with DB (Monolith Container)

A single Docker container running both the Flask ML web application and an internal SQLite database (`predictions.db`) to store prediction history.

## 🚀 How to Run

### 1. Build the Docker Image
```bash
docker build -t iris-webapp-db:s2 .
```

### 2. Run the Container
```bash
docker run -d -p 5000:5000 --name iris-web-db-s2 iris-webapp-db:s2
```

### 3. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 4. Stop and Clean Up
```bash
docker stop iris-web-db-s2 && docker rm iris-web-db-s2
```
