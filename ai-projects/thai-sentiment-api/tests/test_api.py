import pytest
from fastapi.testclient import TestClient

from app.main import app
from sentiment.preprocess import normalise, thai_tokenize


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # "with" runs the startup that loads the model
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_returns_valid_probabilities(client):
    r = client.post("/predict", json={"text": "อาหารอร่อยมาก บริการดีสุดๆ ประทับใจ"})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in {"pos", "neu", "neg", "q"}
    assert abs(sum(body["scores"].values()) - 1.0) < 1e-3
    assert 0 <= body["confidence"] <= 1


def test_obvious_examples(client):
    pos = client.post("/predict", json={"text": "ชอบมากเลยค่ะ ดีมากๆ ประทับใจสุดๆ"}).json()
    neg = client.post("/predict", json={"text": "แย่มาก ห่วยที่สุด ไม่ประทับใจเลย ผิดหวัง"}).json()
    assert pos["label"] == "pos"
    assert neg["label"] == "neg"


def test_batch(client):
    r = client.post("/predict/batch", json={"texts": ["ดีมาก", "แย่มาก"]})
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_validation_errors(client):
    assert client.post("/predict", json={"text": ""}).status_code == 422
    assert client.post("/predict/batch", json={"texts": ["ok", "  "]}).status_code == 422


def test_preprocess():
    assert normalise("ดีมากกกกก http://x.com") == "ดีมากก  "
    assert "อร่อย" in thai_tokenize("อาหารอร่อยมาก")
