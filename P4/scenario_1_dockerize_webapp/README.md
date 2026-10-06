# Scenario 1: Dockerize Webapp

A standalone Dockerized Flask web application that serves an Iris flower classification machine learning model.

## 🚀 How to Run

### 1. Build the Docker Image
```bash
docker build -t iris-webapp:s1 .
```

### 2. Run the Container
```bash
docker run -d -p 5000:5000 --name iris-web-s1 iris-webapp:s1
```

### 3. Open in Browser
Visit: **http://localhost:5000**

### 4. Stop and Clean Up
```bash
docker stop iris-web-s1 && docker rm iris-web-s1
```
