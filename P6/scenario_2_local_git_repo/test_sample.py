import os
import pytest
from app import app, model, CLASS_NAMES

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_model_loaded():
    assert model is not None
    # Sample Iris Setosa feature prediction
    pred = model.predict([[5.1, 3.5, 1.4, 0.2]])
    assert len(pred) == 1
    assert CLASS_NAMES[int(pred[0])] == 'Setosa'

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_prediction_endpoint(client):
    response = client.post('/predict', data={
        'a1': '5.1',
        'a2': '3.5',
        'a3': '1.4',
        'a4': '0.2'
    })
    assert response.status_code == 200
    assert b'Setosa' in response.data

def test_records_page(client):
    response = client.get('/records')
    assert response.status_code == 200
