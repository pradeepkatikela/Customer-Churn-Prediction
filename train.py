# ==========================
# Import Libraries
# ==========================

import warnings
warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from xgboost import XGBClassifier
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
# ==========================
# Data Preprocessing
# ==========================

from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
def preprocess_data(df):

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # Fill missing values
    imputer = SimpleImputer(strategy="mean")
    df["TotalCharges"] = imputer.fit_transform(
        df[["TotalCharges"]]
    )

    # Convert target variable
    df["Churn"] = df["Churn"].map({
        "Yes": 1,
        "No": 0
    })

    return df
df = preprocess_data(df)

print("Preprocessing Completed!")
# ==========================
# Feature Engineering
# ==========================

df["HighMonthlyCharge"] = (df["MonthlyCharges"] > 80).astype(int)

df["HasTechSupport"] = df["TechSupport"].map({
    "Yes": 1,
    "No": 0,
    "No internet service": 0
})

df["HasInternetService"] = df["InternetService"].map({
    "No": 0,
    "DSL": 1,
    "Fiber optic": 1
})
# ==========================
# Define Features
# ==========================

categorical_features = [
    'gender',
    'Partner',
    'Dependents',
    'PhoneService',
    'PaperlessBilling',
    'MultipleLines',
    'InternetService',
    'OnlineSecurity',
    'OnlineBackup',
    'DeviceProtection',
    'TechSupport',
    'StreamingTV',
    'StreamingMovies',
    'Contract',
    'PaymentMethod'
]

numerical_features = [
    'SeniorCitizen',
    'tenure',
    'MonthlyCharges',
    'TotalCharges',
    'HighMonthlyCharge',
    'HasTechSupport',
    'HasInternetService'
]
# ==========================
# Preprocessor
# ==========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "num",
            "passthrough",
            numerical_features
        )
    ]
)
# ==========================
# XGBoost Model
# ==========================

xgb_model = XGBClassifier(
    learning_rate=0.1,
    max_depth=3,
    n_estimators=200,
    scale_pos_weight=2,
    random_state=42,
    eval_metric="logloss"
)

# ==========================
# ML Pipeline
# ==========================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", xgb_model)
    ]
)
# Features and Target
X = df.drop("Churn", axis=1)
y = df["Churn"]
# ==========================
# Train-Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train Shape :", X_train.shape)
print("Test Shape  :", X_test.shape)
# ==========================
# Train Pipeline
# ==========================

pipeline.fit(X_train, y_train)

print("✅ Pipeline trained successfully!")
# ==========================
# Save Pipeline
# ==========================

import os

os.makedirs("models", exist_ok=True)

joblib.dump(pipeline, "models/pipeline.pkl")

print("✅ Pipeline saved successfully!")
# ==========================
# Save Model
# ==========================