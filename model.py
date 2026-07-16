from pathlib import Path
import pandas as pd
import joblib
import numpy as np

CAR_PRICE_API_DIR = Path(__file__).resolve().parent

MODEL_PATH = CAR_PRICE_API_DIR / "xgb_model.pkl"
COLS_PATH = CAR_PRICE_API_DIR / "feature_columns.pkl"
SCALER_PATH = CAR_PRICE_API_DIR / "scaler.pkl"  
_model = None
_feature_columns = None
_scaler = None  


def load_artifacts():
    global _model, _feature_columns, _scaler

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    if _feature_columns is None:
        _feature_columns = joblib.load(COLS_PATH)

    if _scaler is None:  # ✅ ADD THIS
        _scaler = joblib.load(SCALER_PATH)


def preprocess(payload: dict) -> pd.DataFrame:
    data = payload.copy()

    data['Year'] = int(data['Year'])
    data['Present_Price'] = float(data['Present_Price'])
    data['Kms_Driven'] = int(data['Kms_Driven'])
    data['Owner'] = int(data['Owner'])  # Keep as int, NOT string

    df = pd.DataFrame([data])

    # 1. Create Car_Age
    current_year = 2026
    df['Car_Age'] = current_year - df['Year']

    # 2. Drop Car_Name and Year
    df = df.drop('Year', axis=1)
    if 'Car_name' in df.columns:
        df = df.drop('Car_name', axis=1)

    # 3. One-hot encode ONLY Fuel_Type, Seller_Type, Transmission
    #    Owner stays numerical just like in training!
    categorical_cols = ['Fuel_Type', 'Seller_Type', 'Transmission']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 4. Fill missing columns
    for col in _feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # 5. Reorder columns
    df_encoded = df_encoded[_feature_columns]
    df_encoded = df_encoded.astype(float)

    # ✅ 6. Apply StandardScaler to numerical columns (CRITICAL FIX)
    numerical_cols = ['Year', 'Present_Price', 'Kms_Driven', 'Car_Age']
    # Year is dropped, so only scale the ones present
    scale_cols = [col for col in numerical_cols if col in df_encoded.columns]
    df_encoded[scale_cols] = _scaler.transform(df_encoded[scale_cols])

    print(f"Final columns: {df_encoded.columns.tolist()}")
    print(f"Final shape: {df_encoded.shape}")

    return df_encoded


def predict_price(payload: dict) -> float:
    load_artifacts()
    X = preprocess(payload)
    pred = _model.predict(X)[0]
    return float(pred)