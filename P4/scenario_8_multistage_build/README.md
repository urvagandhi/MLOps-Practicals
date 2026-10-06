# Scenario 8: Multi-Stage Build

Demonstrates Docker multi-stage builds to produce a leaner, production-ready image.

- **Builder Stage (`builder`):** Installs Python packages to an isolated prefix (`/install`).
- **Runtime Stage:** Starts from a clean `python:3.12-slim` image, copies only the compiled packages into `/usr/local`, and adds application code. No build tools or wheel caches remain in the final image.

## 🚀 How to Run

### 1. Build the Multi-Stage Image
From `P4/scenario_8_multistage_build/webapp`:
```bash
docker build -t iris-webapp:multistage .
```

### 2. Compare Image Sizes
Compare the multi-stage image against the single-stage image:
```bash
docker images | grep iris-webapp
```

### 3. Run with Docker Compose
From `P4/scenario_8_multistage_build`:
```bash
docker compose up --build -d
```

### 4. Open in Browser
- **Make Predictions:** http://localhost:5000
- **View Records:** http://localhost:5000/records

### 5. Tear Down
```bash
docker compose down
```
