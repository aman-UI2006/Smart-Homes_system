# Smart Homes system

Flask API for energy forecasting (LSTM) with an optional Streamlit dashboard. ML stack: TensorFlow, scikit-learn, pandas.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the API:

```bash
python app.py
```

Run the dashboard (separate terminal):

```bash
streamlit run frontend.py
```

Copy `.env.example` to `.env` and set `GROQ_API_KEY` if you use AI optimization. MySQL is optional.

## Deploy on Render

- Python is pinned to **3.11.9** via `.python-version` so TensorFlow installs (TensorFlow has no wheels for Python 3.14+). See [Render: Python version](https://render.com/docs/python-version).
- Build: `pip install -r requirements.txt`
- Start command comes from the `Procfile` (`gunicorn` binding to `$PORT`).
- Optionally set `PYTHON_VERSION=3.11.9` in the service environment if the repo root differs from the service **Root Directory**.
