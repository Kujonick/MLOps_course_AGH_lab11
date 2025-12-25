from src.inference import load_models, predict
import pytest
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


def test_loading():
    model, classifier = load_models()
    assert isinstance(model, SentenceTransformer)
    assert isinstance(classifier, LogisticRegression)


model, classifier = load_models()


@pytest.mark.parametrize(
    "text", [("This is good wording",), ("This is bad wording",), ("None",)]
)
def test_prediction(text):
    output = predict(model, classifier, text)
    assert output in range(3)
