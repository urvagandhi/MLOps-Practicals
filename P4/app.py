# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for
import os
import pickle

from waitress import serve

app = Flask(__name__)
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

@app.route('/')
def index():
    if request.host == "api.abcd.com:5000" :
        return "On server Block 2"
    else :
        return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'GET':
        # return render_template('index.html')
        return redirect(url_for('index'))
    else :
        sepal_length = float(request.form['a1'])
        sepal_width = float(request.form['a2'])
        petal_length = float(request.form['a3'])
        petal_width = float(request.form['a4'])
        
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        class_names = ['Setosa', 'Versicolor', 'Virginica']
        p_class = class_names[prediction[0]]
        return render_template('prediction.html', prediction=p_class)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    serve(app, host='0.0.0.0', port=5000)