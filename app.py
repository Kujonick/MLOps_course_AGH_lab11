from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import PredictRequest, PredictResponse
from src.inference import predict, load_models

app = FastAPI()

model, classifier = load_models()
responses = ["negative", "neutral", "positive"]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_request(request: PredictRequest):
    if not request.text:
        return JSONResponse(
            content={"message": "Request cannot be empty"}, status_code=400
        )
    output = predict(model, classifier, request.text)
    return PredictResponse(prediction=responses[output])
