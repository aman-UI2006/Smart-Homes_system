# 1. Imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input


# 2. Load dataset
df = pd.read_csv("AEP_hourly.csv")

# 3. Preprocessing
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

data = df['AEP_MW'].values.reshape(-1, 1)


# 4. Scaling
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)


# 5. Create sequences
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)


SEQ_LENGTH = 24   # past 24 hours
X, y = create_sequences(data_scaled, SEQ_LENGTH)


# 6. Train-test split (NO shuffle)
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


# 7. Build LSTM model (CLEAN VERSION)
model = Sequential([
    Input(shape=(SEQ_LENGTH, 1)),
    LSTM(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')


# 8. Train model
print("Training LSTM model...")
model.fit(X_train, y_train, epochs=5, batch_size=32)


# 9. Predictions
pred_scaled = model.predict(X_test)


# 10. Convert back to actual values (MW)
y_test_actual = scaler.inverse_transform(y_test)
pred_actual = scaler.inverse_transform(pred_scaled)


# 11. Print results
print("\nLSTM Predictions (Actual MW):")
print(pred_actual[:5])

mse = mean_squared_error(y_test_actual, pred_actual)
print("\nLSTM MSE:", mse)


# 12. Save model (VERY IMPORTANT for backend)
model.save("lstm_model.h5")
print("\nModel saved as lstm_model.h5")