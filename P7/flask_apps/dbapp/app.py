from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///records.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Metric ---
RECORD_ADDED = Counter("dbapp_records_added_total", "Total number of records added")

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl = db.Column(db.Float)
    sw = db.Column(db.Float)
    pl = db.Column(db.Float)
    pw = db.Column(db.Float)
    pred = db.Column(db.String(50))

@app.route("/add_record", methods=["POST"])
def add_rec():
    record = Prediction(**request.get_json())
    db.session.add(record)
    db.session.commit()
    RECORD_ADDED.inc()
    return jsonify({"message": "Record added successfully."}), 201

@app.route("/records", methods=["GET"])
def get_recs():
    records = Prediction.query.all()
    data = [{"sl": r.sl, "sw": r.sw, "pl": r.pl, "pw": r.pw, "prediction": r.pred} for r in records]
    return jsonify(data)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8001, debug=True)
