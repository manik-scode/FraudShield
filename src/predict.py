import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

model = joblib.load(ARTIFACT_DIR / "random_forest_model.joblib")
encoder = joblib.load(ARTIFACT_DIR / "encoder.joblib")
merchant_map = joblib.load(ARTIFACT_DIR / "merchant_map.joblib")
feature_columns = joblib.load(ARTIFACT_DIR / "feature_columns.joblib")


class PredictPipeline:

    def __init__(self):
        pass

    def predict(self, input_data):


        df = pd.DataFrame([input_data])



        df["merchant"] = (
            df["merchant"]
            .map(merchant_map)
            .fillna(0)
            .astype(int)
        )



        weekday_map = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }

        df["transaction_weekday"] = df["transaction_weekday"].map(weekday_map)



        df["is_night_transaction"] = (
            df["is_night_transaction"]
            .astype(int)
        )



        encoded = encoder.transform(df[["category"]])

        encoded_df = pd.DataFrame(
            encoded,
            columns=encoder.get_feature_names_out(["category"]),
            index=df.index
        )

        df = pd.concat(
            [
                df.drop(columns=["category"]),
                encoded_df
            ],
            axis=1
        )



        for col in feature_columns:

            if col not in df.columns:

                df[col] = 0


        df = df[feature_columns]

        fraud_probability = float(model.predict_proba(df)[0][1])
        THRESHOLD = 0.25 
        
        prediction = 1 if fraud_probability >= THRESHOLD else 0



        fraud_probability = float(model.predict_proba(df)[0][1])
        if fraud_probability >= THRESHOLD:
            prediction = "Fraud"
        else:
            prediction = "Not Fraud"

        return {
        "prediction": prediction,
        "fraud_probability": fraud_probability
    }
