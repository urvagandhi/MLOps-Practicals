import os
import pickle
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_SERVICE_URL = os.environ.get("DB_SERVICE_URL", "http://dbcnt:5000")

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

CLASS_NAMES = ['Setosa', 'Versicolor', 'Virginica']

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

    # Send record to DB microservice
    try:
        requests.post(f"{DB_SERVICE_URL}/add_record", json={
            "a1": sepal_length,
            "a2": sepal_width,
            "a3": petal_length,
            "a4": petal_width,
            "prediction": p_class
        }, timeout=3)
    except Exception as e:
        print(f"Could not connect to DB service at {DB_SERVICE_URL}: {e}")

    return render_template('prediction.html', prediction=p_class)

@app.route('/records')
def records():
    records_list = []
    try:
        resp = requests.get(f"{DB_SERVICE_URL}/records", timeout=3)
        if resp.status_code == 200:
            records_list = resp.json()
    except Exception as e:
        print(f"Could not connect to DB service at {DB_SERVICE_URL}: {e}")
    
    return render_template('records.html', records=records_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
