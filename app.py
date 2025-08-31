import joblib
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

# Load model
MODEL_PATH = "sms_spam_pipeline_lr.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="SMS Spam Detection API", version="1.0.0")

class SMSRequest(BaseModel):
    message: str

def to_label(pred):
    if isinstance(pred, str):
        return pred
    return "spam" if int(pred) == 1 else "ham"

@app.get("/")
def home():
    return {"message": "Welcome to SMS Spam Detection API"}

@app.get("/predict")
def predict_get(message: str = Query(..., description="SMS message to classify")):
    try:
        pred = model.predict([message])[0]
        return {"message": message, "prediction": to_label(pred)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@app.post("/predict")
def predict_post(data: SMSRequest):
    try:
        pred = model.predict([data.message])[0]
        return {"message": data.message, "prediction": to_label(pred)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")