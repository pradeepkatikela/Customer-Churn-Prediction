from fastapi import FastAPI

from backend.schema import CustomerData
from backend.model_loader import predict

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a customer will churn.",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is Running!"
    }


@app.post("/predict")
def predict_churn(customer: CustomerData):

    prediction, probability = predict(customer.model_dump())

    return {
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "churn_probability": round(float(probability), 4)
    }