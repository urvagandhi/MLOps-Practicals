# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for
import pickle

from waitress import serve

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# Scenario 6 : 2 app.py, 2 serverblock,
@app.route('/')
def index():
    return "How are u ? I'm on Different App.py and Different Port and Different Server Block"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    # serve(app, host='0.0.0.0', port=5001)