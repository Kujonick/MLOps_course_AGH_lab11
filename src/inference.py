from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import joblib
from typing import Tuple
from src.scripts.settings import Settings

def load_models(settings: Settings) -> Tuple[SentenceTransformer, LogisticRegression]:
    model = SentenceTransformer(str(settings.sentence_transformer_dir))
    classifier: LogisticRegression = joblib.load(str(settings.classifier_joblib_path))
    return model, classifier


def predict(model: SentenceTransformer, classifier: LogisticRegression, text: str):
    print(text)
    embedding = model.encode(text).reshape(1, -1)
    output = classifier.predict(embedding)
    print(output)
    return output[0]
