import joblib
import pandas as pd

pipeline = joblib.load("models/pipeline.pkl")


def predict(customer_data: dict):

    # Convert to DataFrame
    df = pd.DataFrame([customer_data])

    # -------------------------
    # Feature Engineering
    # -------------------------

    df["HighMonthlyCharge"] = (
        df["MonthlyCharges"] > 80
    ).astype(int)

    df["HasTechSupport"] = (
        df["TechSupport"] == "Yes"
    ).astype(int)

    df["HasInternetService"] = (
        df["InternetService"] != "No"
    ).astype(int)

    # -------------------------

    prediction = pipeline.predict(df)[0]

    probability = pipeline.predict_proba(df)[0][1]

    return prediction, probability