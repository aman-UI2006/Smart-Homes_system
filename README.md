# 🏠 Smart Homes Energy Prediction System

## 🚀 Live Demo
- 🌐 **Frontend (Streamlit App):**  
  https://smart-homessystem-brsy2muq9mhlbw9xgmtwrn.streamlit.app/

- ⚙️ **Backend (Render API):**  
  https://smart-homes-system.onrender.com/

---

## 💡 Project Idea

The **Smart Homes Energy Prediction System** is an AI-powered web application designed to predict energy consumption in smart homes using machine learning.

### 🔥 Core Idea:
- Analyze historical energy usage data
- Predict future energy consumption using an LSTM model
- Help users optimize energy usage and reduce electricity costs

### 🎯 Goals:
- Smart energy monitoring  
- AI-based forecasting  
- Efficient resource utilization  
- Real-time prediction interface  

---

## 🧠 Features

- 📊 Energy consumption prediction using AI  
- ⚡ LSTM deep learning model  
- 🌐 Interactive frontend using Streamlit  
- 🔗 Backend API using Flask  
- 📈 Real-time prediction results  
- 💾 Data preprocessing and handling  

---

## 🛠️ Tech Stack

### 🔹 Frontend
- Streamlit  

### 🔹 Backend
- Flask (Python)  

### 🔹 Machine Learning
- TensorFlow / Keras (LSTM Model)  
- Scikit-learn  
- NumPy  
- Pandas  

### 🔹 Deployment
- Streamlit Cloud (Frontend)  
- Render (Backend)  

### 🔹 Tools
- Git & GitHub  
- REST API  

---

## 📂 Project Structure

```
Smart-Homes_system/
│
├── app.py                # Flask backend
├── lstm_model.h5         # Trained ML model
├── scaler.pkl            # Data scaler
├── AEP_hourly.csv        # Dataset
├── requirements.txt
│
├── frontend/
│   └── streamlit_app.py
│
└── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Smart-Homes_system.git
cd Smart-Homes_system
```

---

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Backend (Flask API)
```bash
python app.py
```

Backend runs on:
```
http://127.0.0.1:5000/
```

---

### 5️⃣ Run Frontend (Streamlit)
```bash
streamlit run streamlit_app.py
```

---

## 🔗 API Configuration

In your Streamlit app:

```python
API_URL = "https://smart-homes-system.onrender.com"
```

For local testing:

```python
API_URL = "http://127.0.0.1:5000"
```

---

## 📊 How It Works

1. User inputs energy data via frontend  
2. Streamlit sends request to Flask API  
3. Backend processes input using:
   - Scaler  
   - LSTM Model  
4. Prediction is generated  
5. Result is displayed on frontend  

---

## 🧪 Model Details

- Model Type: LSTM (Long Short-Term Memory)  
- Use Case: Time-series forecasting  
- Input: Historical energy consumption  
- Output: Predicted energy usage  

---

## 🚀 Future Improvements

- 🔐 User authentication system  
- 📱 Mobile-friendly UI  
- 📊 Advanced analytics dashboard  
- ☁️ Cloud database integration  
- 🤖 Auto model retraining  

---

## 🤝 Contributing

Contributions are welcome!

```
Fork → Clone → Create Branch → Commit → Push → Pull Request
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Aman Pokale**  
- Computer Engineering Student  
- AI & Startup Enthusiast 🚀  

---
