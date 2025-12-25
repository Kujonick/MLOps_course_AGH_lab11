from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import joblib
from typing import Tuple
import os
LOCAL_DIR = os.getenv("LOCAL_DIR")


def load_models() -> Tuple[SentenceTransformer, LogisticRegression]:
    model = SentenceTransformer(f"{LOCAL_DIR}/sentence_transformer.model")
    classifier: LogisticRegression = joblib.load(f"{LOCAL_DIR}/classifier.joblib")
    return model, classifier


def predict(model: SentenceTransformer, classifier: LogisticRegression, text: str):
    print(text)
    embedding = model.encode(text).reshape(1, -1)
    output = classifier.predict(embedding)
    print(output)
    return output[0]
