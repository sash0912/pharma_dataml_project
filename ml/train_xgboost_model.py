import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

FEATURE_FILE = "data/features/sales_features_monthly.csv"
MODEL_PATH = "ml/models/xgboost_model.pkl"

df = pd.read_csv(FEATURE_FILE)

df = df.sort_values(["product", "month"])

#
feature_cols = [
    "lag_1",
    "lag_3",
    "lag_6",
    "lag_12",
    "rolling_mean_3",
    "rolling_mean_6",
    "rolling_std_3"
]

X = df[feature_cols]
y = df["qty"]

split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("XGBoost Performance")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")

joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
