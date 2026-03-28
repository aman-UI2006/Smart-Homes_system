import html
import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

# ===============================
# 🔥 BACKEND URL (IMPORTANT)
# ===============================
API_URL = "https://smart-homes-system.onrender.com"

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Smart Energy Dashboard",
    layout="wide"
)

# ===============================
# Title
# ===============================
st.title("⚡ Smart Energy Forecast Dashboard")

# ===============================
# SESSION STATE
# ===============================
if "energy_values" not in st.session_state:
    st.session_state.energy_values = [14000.0] * 24

for i in range(24):
    if f"input_{i}" not in st.session_state:
        st.session_state[f"input_{i}"] = st.session_state.energy_values[i]

# ===============================
# INPUT GRID
# ===============================
st.subheader("📊 Hourly Energy Input (24 Hours)")

values = []
cols = st.columns(6)

for i in range(24):
    with cols[i % 6]:
        val = st.number_input(
            f"H{i + 1}",
            value=float(st.session_state[f"input_{i}"]),
            key=f"input_{i}",
        )
        values.append(val)

st.session_state.energy_values = values

# ===============================
# CHART
# ===============================
st.subheader("📈 Load Profile")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(range(1, 25), values, marker="o")
ax.set_xlabel("Hour")
ax.set_ylabel("Energy (MW)")
ax.grid(True)

st.pyplot(fig)

# ===============================
# APPLIANCES INPUT
# ===============================
st.subheader("🏠 Appliance Usage (kWh)")

col1, col2 = st.columns(2)

with col1:
    appliances = {
        "AC": st.number_input("AC", value=2.0),
        "Fridge": st.number_input("Fridge", value=1.0),
        "Washing Machine": st.number_input("Washing Machine", value=0.5),
        "Lights": st.number_input("Lights", value=0.8),
    }

with col2:
    appliances.update({
        "Fans": st.number_input("Fans", value=0.6),
        "TV": st.number_input("TV", value=0.4),
        "Laptop": st.number_input("Laptop", value=0.3),
        "Others": st.number_input("Others", value=0.5),
    })

# ===============================
# ACTION BUTTONS
# ===============================
st.subheader("⚙️ Actions")

col1, col2 = st.columns(2)

prediction = None
status = None
suggestion = None
ai_suggestion = None

# 🔹 Forecast
with col1:
    if st.button("🔮 Generate Forecast"):
        try:
            res = requests.post(
                f"{API_URL}/predict",
                json={"input": values},
                timeout=60,
            )
            res.raise_for_status()
            prediction = res.json()["prediction_MW"]
        except Exception as e:
            st.error(f"Error: {e}")

# 🔹 Optimize
with col2:
    if st.button("⚡ Run Optimization"):
        try:
            res = requests.post(
                f"{API_URL}/optimize",
                json={"input": values, "appliances": appliances},
                timeout=120,
            )
            res.raise_for_status()
            data = res.json()

            prediction = data["prediction_MW"]
            status = data["status"]
            suggestion = data["suggestion"]
            ai_suggestion = data.get("ai_suggestion", "")

        except Exception as e:
            st.error(f"Error: {e}")

# ===============================
# RESULTS
# ===============================
if prediction:
    st.success(f"🔋 Prediction: {prediction:.2f} MW")

if status:
    st.info(f"⚙️ Status: {status}")

if suggestion:
    st.warning(f"💡 Suggestion: {suggestion}")

if ai_suggestion:
    st.subheader("🤖 AI Smart Suggestions")
    st.write(ai_suggestion)

# ===============================
# HISTORY
# ===============================
st.subheader("📜 History")

if st.button("🔄 Load History"):
    try:
        res = requests.get(f"{API_URL}/history")
        res.raise_for_status()
        data = res.json()

        if len(data) == 0:
            st.info("No history yet")
        else:
            st.dataframe(pd.DataFrame(data))

    except Exception as e:
        st.error(f"Error: {e}")