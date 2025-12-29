from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import PredictRequest, PredictResponse
from src.inference import predict, load_models
from src.scripts.download_artifacts import load_artifacts
from src.scripts.settings import Settings
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

settings = Settings()
load_artifacts(settings)
app = FastAPI()

tokenizer, model, classifier = load_models(settings)
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
    output = predict(tokenizer, model, classifier, request.text)
    return PredictResponse(prediction=responses[output])


handler = Mangum(app)