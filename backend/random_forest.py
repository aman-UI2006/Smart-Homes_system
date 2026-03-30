# 1. Imports
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
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

# Remove NaN values created by lag
df = df.dropna()

# 5. Define Features and Target
X = df[['lag1', 'lag2', 'lag3', 'hour', 'dayofweek']]
y = df['AEP_MW']

# 6. Train-test split (NO shuffle for time series)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# 7. Model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# 8. Prediction
pred = model.predict(X_test)

print("Random Forest Predictions:", pred[:5])

# 9. Evaluation
mse = mean_squared_error(y_test, pred)
print("MSE:", mse)