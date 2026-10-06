import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, 'records.db')

def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                a1 REAL,
                a2 REAL,
                a3 REAL,
                a4 REAL,
                prediction TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

init_db()

@app.route('/')
def health():
    return jsonify({"service": "dbapp", "status": "running"})

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json() or {}
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            'INSERT INTO predictions (a1, a2, a3, a4, prediction) VALUES (?, ?, ?, ?, ?)',
            (float(data.get('a1', 0)), float(data.get('a2', 0)),
             float(data.get('a3', 0)), float(data.get('a4', 0)),
             str(data.get('prediction', '')))
        )
        new_id = cursor.lastrowid
    return jsonify({"status": "success", "id": new_id}), 201

@app.route('/records', methods=['GET'])
def get_records():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM predictions ORDER BY id DESC').fetchall()
        records_list = [dict(r) for r in rows]
    return jsonify(records_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
