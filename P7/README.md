# Practical 7: Prometheus & Grafana Monitoring

Complete Monitoring and Alerting setup for ML web application (`webapp`), SQLite database service (`dbapp`), Prometheus metrics server, Alertmanager, Node/Windows Exporter, and Grafana Dashboard.

---

## 📁 Directory Structure

```text
P7/
├── docker-compose.yml              # Single-command orchestrator for all 6 services
├── requirements.txt                # Python dependencies
├── prometheus/
│   ├── prometheus.yml              # Scrape configuration
│   └── rules.yml                   # Recording & alert rules (High CPU, WebApp slow, DB down)
├── alertmanager/
│   └── alertmanager.yml            # Alert routing & notification config
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── prometheus.yml      # Automatic Prometheus data source connection
└── flask_apps/
    ├── webapp/
    │   ├── app.py                  # Iris web app with Prometheus metrics (Port 8000)
    │   ├── make_model.py           # Trains RandomForest & saves model.pkl
    │   ├── model.pkl               # Serialized model
    │   ├── Dockerfile
    │   └── templates/
    │       └── index.html          # Web UI prediction form
    └── dbapp/
        ├── app.py                  # Prediction logging database API (Port 8001)
        └── Dockerfile
```

---

## 🚀 Running on macOS / Linux via Docker Compose (Recommended)

To start the entire monitoring stack with a single command:

```bash
cd P7
docker compose up -d --build
```

### Services & URLs:

| Service | Host Port | Description |
|---|---|---|
| **Iris Web App** | [http://localhost:8000](http://localhost:8000) | Frontend for predictions & `/metrics` |
| **DB App** | [http://localhost:8001/records](http://localhost:8001/records) | Prediction records & `/metrics` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Targets, metrics explorer, rules, and alerts |
| **Alertmanager** | [http://localhost:9093](http://localhost:9093) | Alert notification dashboard |
| **Node Exporter** | [http://localhost:9100/metrics](http://localhost:9100/metrics) | System resource metrics |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Dashboards (Login: `admin` / `admin`) |

---

## 💻 Running Directly with Local Python Virtualenv

### 1. Run DB App
```bash
cd flask_apps/dbapp
python app.py
```

### 2. Run Web App
```bash
cd flask_apps/webapp
python make_model.py   # Run once if model.pkl is missing
python app.py
```

---

## 📊 Verification & Health Check

1. **Prometheus Targets**: Open [http://localhost:9090/targets](http://localhost:9090/targets) (verify all endpoints are `UP`).
2. **Prometheus Rules**: Open [http://localhost:9090/rules](http://localhost:9090/rules) (verify `system:cpu_usage_percent`, `HighCPUUsage`, `WebAppLatencyHigh`, `DBAppDown`).
3. **Grafana**: Open [http://localhost:3000](http://localhost:3000) (Data source `Prometheus` is pre-configured).
