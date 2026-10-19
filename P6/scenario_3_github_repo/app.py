import os
import pickle
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, 'model.pkl')
db_path = os.path.join(BASE_DIR, 'predictions.db')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

CLASS_NAMES = ['Setosa', 'Versicolor', 'Virginica']

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
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    sepal_length = float(request.form['a1'])
    sepal_width = float(request.form['a2'])
    petal_length = float(request.form['a3'])
    petal_width = float(request.form['a4'])
    
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    p_class = CLASS_NAMES[int(prediction[0])]

    # Insert into SQLite database
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            'INSERT INTO predictions (a1, a2, a3, a4, prediction) VALUES (?, ?, ?, ?, ?)',
            (sepal_length, sepal_width, petal_length, petal_width, p_class)
        )

    return render_template('prediction.html', prediction=p_class)

@app.route('/records')
def records():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM predictions ORDER BY id DESC').fetchall()
        records_list = [dict(r) for r in rows]
    return render_template('records.html', records=records_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
