import os
import pickle
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    return render_template('prediction.html', prediction=p_class)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
