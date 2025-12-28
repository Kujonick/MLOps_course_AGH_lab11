from src.inference import load_models, predict
import pytest
import onnxruntime as ort
from tokenizers import Tokenizer

from src.scripts.settings import Settings

def test_loading():
    settings = Settings()
    tokenizer, model, classifier = load_models(settings)
    assert isinstance(model, ort.InferenceSession)
    assert isinstance(classifier, ort.InferenceSession)
    assert isinstance(tokenizer, Tokenizer)

settings = Settings()
tokenizer, model, classifier = load_models(settings)


@pytest.mark.parametrize(
    "text", ["This is good wording", "This is bad wording", "None"]
)
def test_prediction(text):
    output = predict(tokenizer, model, classifier, text)
    assert output in range(3)
