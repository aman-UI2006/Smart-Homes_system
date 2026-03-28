# 1. Imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 2. Load dataset
df = pd.read_csv("AEP_hourly.csv")

# 3. Preprocessing
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

# 4. Feature Engineering (VERY IMPORTANT)

# Lag features (past values)
df['lag1'] = df['AEP_MW'].shift(1)
df['lag2'] = df['AEP_MW'].shift(2)
df['lag3'] = df['AEP_MW'].shift(3)

# Time features
df['hour'] = df['Datetime'].dt.hour
df['dayofweek'] = df['Datetime'].dt.dayofweek

# Drop NaN values (created by lag)
df = df.dropna()

# 5. Define Features & Target
X = df[['lag1', 'lag2', 'lag3', 'hour', 'dayofweek']]
y = df[['AEP_MW']]   # keep as 2D for scaler

# 6. Scaling (IMPORTANT)
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# 7. Train-test split (NO shuffle for time series)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_scaled, test_size=0.2, shuffle=False
)

# 8. Model
model = LinearRegression()
model.fit(X_train, y_train)

# 9. Prediction
pred_scaled = model.predict(X_test)

# 10. Convert back to actual values (MW)
y_test_actual = scaler_y.inverse_transform(y_test)
pred_actual = scaler_y.inverse_transform(pred_scaled)

# 11. Print Predictions
print("Predictions (Actual MW):", pred_actual[:5])

# 12. Evaluation
mse = mean_squared_error(y_test_actual, pred_actual)
print("MSE:", mse)