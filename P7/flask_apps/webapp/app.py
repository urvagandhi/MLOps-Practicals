from flask import Flask, request, render_template
import pickle, os, numpy as np, requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
DB_SERVICE_URL = os.environ.get("DB_SERVICE_URL", "http://localhost:8001/add_record")

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# --- Metrics ---
REQUEST_COUNT = Counter("webapp_request_count", "Total requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("webapp_request_latency_seconds", "Request latency", ["endpoint"])

@app.before_request
def before_request():
    REQUEST_COUNT.labels(request.method, request.path).inc()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@REQUEST_LATENCY.labels("/predict").time()
def make_pred():
    sl, sw, pl, pw = map(float, [request.form[x] for x in ["sl", "sw", "pl", "pw"]])
    pred = model.predict(np.array([[sl, sw, pl, pw]]))
    try:
        requests.post(DB_SERVICE_URL, json={"sl": sl, "sw": sw, "pl": pl, "pw": pw, "pred": str(pred[0])}, timeout=3)
    except Exception as e:
        print(f"Warning: Could not connect to DB service: {e}")
    return str(pred[0])

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
