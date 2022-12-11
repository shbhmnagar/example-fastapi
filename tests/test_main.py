from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root():
    res = client.get('/')
    assert res.json().get('message') == 'Welcome to my FASTAPI.'
    assert res.status_code == 200