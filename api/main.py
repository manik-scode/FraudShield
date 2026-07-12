from fastapi import FastAPI
from pydantic import BaseModel

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict import PredictPipeline

app = FastAPI(
    title="FraudShield API",
    version="1.0"
)



class TransactionData(BaseModel):

    merchant: str
    category: str
    amt: float

    age: int

    transaction_hours: int
    transaction_day: int
    transaction_month: int
    transaction_weekday: str

    is_night_transaction: bool

    merchant_distance: float
    previous_avg_amt: float
    amount_difference: float
    merchant_visit_frequency: int


@app.get("/")
def home():

    return {
        "message": "FraudShield API Running Successfully 🚀"
    }




@app.post("/predict")
def predict(data: TransactionData):

    pipeline = PredictPipeline()

    result = pipeline.predict(data.dict())

    return result