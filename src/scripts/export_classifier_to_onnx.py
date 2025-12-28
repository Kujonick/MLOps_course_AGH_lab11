import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from pathlib import Path

from src.scripts.settings import Settings


def export_classifier_to_onnx(settings: Settings):
    print(f"Loading classifier from {settings.classifier_joblib_path}...")
    classifier = joblib.load(settings.classifier_joblib_path)

    # define input shape: (batch_size, embedding_dim)
    initial_type = [("float_input", FloatTensorType([None, settings.embedding_dim]))]

    print("Converting to ONNX...")
    onnx_model = convert_sklearn(
        model=classifier,
        initial_types=initial_type,
        target_opset=17,
    )  # TODO: complete conversion here

    print(f"Saving ONNX model to {settings.onnx_classifier_path}...")
    # TODO: save the onnx_model to settings.onnx_classifier_path    
    output_path = Path(settings.onnx_classifier_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print("ONNX export completed successfully.")