from fastapi.testclient import TestClient
import pytest
from app import app


@pytest.mark.parametrize(
    "text, status_code", [("", 400), ("This is bad wording", 200), ("None", 200)]
)
def test_predict(text, status_code):
    client = TestClient(app)
    response = client.post("/predict", json={"text": text})
    assert response.status_code == status_code
    assert "prediction" in response.json() if status_code == 200 else True
