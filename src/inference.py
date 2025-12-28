import onnxruntime as ort
from typing import Tuple
from src.scripts.settings import Settings
from tokenizers import Tokenizer
import numpy as np


def load_models(settings: Settings) -> Tuple[Tokenizer, ort.InferenceSession, ort.InferenceSession]:
    tokenizer = Tokenizer.from_file(str(settings.onnx_tokenizer_dir / 'tokenizer.json'))
    model_session = ort.InferenceSession(str(settings.onnx_embedding_model_path))
    classifier_session = ort.InferenceSession(str(settings.onnx_classifier_path))
    return tokenizer, model_session, classifier_session


def predict(tokenizer: Tokenizer, model_session: ort.InferenceSession, classifier_session: ort.InferenceSession, text: str) -> int:
    # tokenize input
    encoded = tokenizer.encode(text)

    # prepare numpy arrays for ONNX
    input_ids = np.array([encoded.ids])
    attention_mask = np.array([encoded.attention_mask])

    # run embedding inference
    embedding_inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
    embeddings: np.ndarray = model_session.run(None, embedding_inputs)[0]

    # run classifier inference
    classifier_input_name = classifier_session.get_inputs()[0].name
    classifier_inputs = {classifier_input_name: embeddings.astype(np.float32)}
    prediction = classifier_session.run(None, classifier_inputs)[0]

    return int(prediction.item())
