import html
import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

API_URL = "https://smart-homes-system.onrender.com"

st.set_page_config(
    page_title="Energy Forecast · Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon=":material/monitoring:",
)

try:
    _IS_DARK = st.context.theme.type == "dark"
except Exception:
    _IS_DARK = False

# -------------------------------
# Design tokens & global stylesheet (Light / Dark aware)
# -------------------------------
_ROOT_LIGHT = """
    :root {
        --bg-page: #ffffff;
        --bg-subtle: #f8fafc;
        --border: #e2e8f0;
        --border-strong: #cbd5e1;
        --text: #0f172a;
        --text-muted: #475569;
        --text-soft: #334155;
        --primary: #171717;
        --primary-hover: #000000;
        --primary-ring: rgba(0, 0, 0, 0.35);
        --accent-indigo: #4f46e5;
        --ok: #059669;
        --warn: #d97706;
        --bad: #dc2626;
        --upload-btn-fg: #0f172a;
        --upload-btn-bg: #f1f5f9;
        --upload-btn-border: #94a3b8;
        --upload-hover-bg: #eef2ff;
        --upload-hover-border: #a5b4fc;
        --header-bg: #ffffff;
        --hero-surface: #ffffff;
        --hero-badge-bg: #eef2ff;
        --hero-badge-border: #c7d2fe;
    }
"""

_ROOT_DARK = """
    :root {
        --bg-page: #161b22;
        --bg-subtle: #21262d;
        --border: #30363d;
        --border-strong: #484f58;
        --text: #f0f6fc;
        --text-muted: #8b949e;
        --text-soft: #c9d1d9;
        --primary: #f0f6fc;
        --primary-hover: #ffffff;
        --primary-ring: rgba(240, 246, 252, 0.25);
        --accent-indigo: #818cf8;
        --ok: #3fb950;
        --warn: #d29922;
        --bad: #f85149;
        --upload-btn-fg: #f0f6fc;
        --upload-btn-bg: #30363d;
        --upload-btn-border: #6e7681;
        --upload-hover-bg: rgba(56, 139, 253, 0.12);
        --upload-hover-border: rgba(56, 139, 253, 0.45);
        --header-bg: rgba(13, 17, 23, 0.92);
        --hero-surface: linear-gradient(135deg, #21262d 0%, #161b22 50%, #1c2128 100%);
        --hero-badge-bg: rgba(129, 140, 248, 0.15);
        --hero-badge-border: rgba(129, 140, 248, 0.4);
    }
"""

_CONTAINER_LIGHT = """
    [data-testid="stAppViewContainer"] {
        position: relative !important;
        overflow: auto !important;
        color-scheme: light;
        background: #ffffff !important;
        background-size: auto !important;
        animation: none !important;
    }
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        display: none !important;
    }
"""

_CONTAINER_DARK = """
    [data-testid="stAppViewContainer"] {
        position: relative !important;
        overflow: auto !important;
        color-scheme: dark;
        background: linear-gradient(
            125deg,
            #0d1117,
            #161b22,
            #1c2128,
            #0d1117,
            #010409
        ) !important;
        background-size: 400% 400% !important;
        animation: bg-gradient-flow 25s ease-in-out infinite !important;
    }
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        inset: -35%;
        min-height: 120%;
        z-index: 0;
        pointer-events: none;
        opacity: 0.9;
        background:
            radial-gradient(ellipse 50% 42% at 15% 25%, rgba(99, 102, 241, 0.12) 0%, transparent 52%),
            radial-gradient(ellipse 48% 46% at 88% 78%, rgba(56, 139, 253, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 42% 48% at 55% 8%, rgba(139, 148, 158, 0.1) 0%, transparent 48%);
        animation: bg-drift 28s ease-in-out infinite;
        will-change: transform;
    }
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: absolute;
        inset: 0;
        min-height: 100%;
        z-index: 0;
        pointer-events: none;
        opacity: 0.25;
        mix-blend-mode: lighten;
        background:
            linear-gradient(
                105deg,
                transparent 0%,
                rgba(255, 255, 255, 0.06) 50%,
                transparent 100%
            );
        background-size: 200% 200%;
        animation: bg-shimmer-slide 12s linear infinite;
    }
"""

_THEME_STYLE_REST = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

    ___ROOT_VARS___

    html, body, [class*="css"] {
        font-family: "DM Sans", system-ui, -apple-system, sans-serif;
    }

    /* Streamlit widgets keep theme contrast; custom sections use :root vars above */

    @keyframes bg-gradient-flow {
        0% { background-position: 0% 40%; }
        25% { background-position: 100% 60%; }
        50% { background-position: 100% 40%; }
        75% { background-position: 0% 60%; }
        100% { background-position: 0% 40%; }
    }

    @keyframes bg-drift {
        0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); opacity: 0.6; }
        25% { transform: translate(6%, -4%) rotate(1deg) scale(1.06); opacity: 0.85; }
        50% { transform: translate(-4%, 5%) rotate(-0.5deg) scale(1.04); opacity: 0.7; }
        75% { transform: translate(3%, 3%) rotate(0.5deg) scale(1.05); opacity: 0.8; }
    }

    @keyframes bg-shimmer-slide {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 200%; }
    }

    ___CONTAINER_BG___

    .stApp {
        background: transparent !important;
    }

    section.main > div {
        max-width: 100%;
    }

    [data-testid="stHeader"] {
        position: relative;
        z-index: 2;
        background: var(--header-bg) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1280px;
    }

    .app-hero {
        padding: 1.5rem 1.5rem 1.35rem 1.5rem;
        margin-bottom: 2rem;
        background: var(--hero-surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }

    .app-hero h1 {
        font-size: clamp(1.75rem, 4vw, 2.125rem);
        font-weight: 600;
        letter-spacing: -0.02em;
        color: var(--text);
        margin: 0 0 0.5rem 0;
    }

    .app-hero p {
        font-size: 1rem;
        color: var(--text-muted);
        margin: 0;
        font-weight: 400;
        max-width: 42rem;
    }

    .app-hero-badge {
        display: inline-block;
        font-size: 0.6875rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text);
        background: var(--hero-badge-bg);
        border: 1px solid var(--hero-badge-border);
        padding: 0.35rem 0.65rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 2rem 0 0.75rem 0;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-top: 0 !important;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }

    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: 1fr; }
    }

    .kpi-card {
        background: var(--bg-page);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem 1.35rem;
        text-align: left;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    }

    .kpi-card h4 {
        font-size: 0.8125rem;
        font-weight: 500;
        color: var(--text-muted);
        margin: 0 0 0.5rem 0;
        text-transform: none;
        letter-spacing: 0;
    }

    .kpi-card .value-green {
        color: var(--ok);
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .kpi-card .value-yellow {
        color: var(--warn);
        font-size: 1.35rem;
        font-weight: 600;
        margin: 0;
    }
    .kpi-card .value-red {
        color: var(--bad);
        font-size: 1.35rem;
        font-weight: 600;
        margin: 0;
    }

    .kpi-card .body-text {
        color: var(--text-soft);
        font-size: 0.9375rem;
        line-height: 1.55;
        margin: 0;
    }

    div.stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 0.95rem;
        font-weight: 700 !important;
        letter-spacing: 0.055em;
        text-transform: none;
        border-radius: 10px;
        border: 1px solid #262626 !important;
        background: linear-gradient(175deg, #3a3a3a 0%, #1a1a1a 45%, #0a0a0a 100%) !important;
        color: #ffffff !important;
        text-shadow:
            0 0 20px rgba(255, 255, 255, 0.5),
            0 0 8px rgba(255, 255, 255, 0.35),
            0 1px 0 rgba(255, 255, 255, 0.75),
            0 -1px 2px rgba(0, 0, 0, 0.5) !important;
        box-shadow:
            0 3px 10px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.22),
            inset 0 -2px 6px rgba(0, 0, 0, 0.35);
        transition: background 0.22s ease, border-color 0.22s ease, transform 0.18s ease, box-shadow 0.22s ease, text-shadow 0.22s ease;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 0.055em !important;
        text-shadow:
            0 0 22px rgba(255, 255, 255, 0.55),
            0 0 10px rgba(255, 255, 255, 0.4),
            0 1px 0 rgba(255, 255, 255, 0.85) !important;
    }

    div.stButton > button:hover {
        border-color: #404040 !important;
        background: linear-gradient(175deg, #525252 0%, #2d2d2d 45%, #171717 100%) !important;
        transform: translateY(-2px);
        box-shadow:
            0 12px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.28),
            inset 0 -2px 6px rgba(0, 0, 0, 0.25);
        text-shadow:
            0 0 28px rgba(255, 255, 255, 0.65),
            0 0 12px rgba(255, 255, 255, 0.45),
            0 1px 0 rgba(255, 255, 255, 0.95),
            0 -1px 1px rgba(0, 0, 0, 0.4) !important;
    }

    div.stButton > button:hover p,
    div.stButton > button:hover span {
        text-shadow:
            0 0 30px rgba(255, 255, 255, 0.7),
            0 0 14px rgba(255, 255, 255, 0.5),
            0 1px 0 rgba(255, 255, 255, 1) !important;
    }

    div.stButton > button:active {
        transform: translateY(0);
    }

    div.stButton > button:focus-visible {
        outline: none !important;
        box-shadow:
            0 0 0 3px var(--primary-ring),
            0 4px 20px rgba(0, 0, 0, 0.35) !important;
    }

    /* Widgets */
    [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: var(--border-strong) !important;
        background-color: var(--bg-page) !important;
    }

    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stFileUploader"] label,
    label[data-testid="stWidgetLabel"] p {
        color: var(--text-soft) !important;
    }

    [data-testid="stNumberInput"] input {
        border-radius: 10px !important;
        border: 1px solid var(--border-strong) !important;
        background: var(--bg-page) !important;
        color: var(--text) !important;
    }

    [data-testid="stNumberInput"] button {
        border-color: var(--border-strong) !important;
        background: var(--bg-subtle) !important;
        color: var(--text-soft) !important;
    }

    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] section {
        padding: 1.5rem !important;
        background: var(--bg-subtle) !important;
        border: 1px dashed var(--border-strong) !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] section:hover {
        border-color: var(--upload-hover-border) !important;
        background: var(--upload-hover-bg) !important;
    }

    /* Browse files + upload controls: explicit contrast both themes */
    [data-testid="stFileUploader"] [data-baseweb="button"],
    [data-testid="stFileUploader"] button {
        color: var(--upload-btn-fg) !important;
        background-color: var(--upload-btn-bg) !important;
        border: 1px solid var(--upload-btn-border) !important;
    }

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"],
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
        color: var(--text) !important;
        opacity: 1 !important;
    }

    /* BaseWeb: match theme text (Streamlit primary widgets) */
    [data-baseweb="select"] span,
    [data-baseweb="popover"] li,
    [data-baseweb="input"] input {
        color: var(--text) !important;
    }

    /* Alerts & tables: follow Streamlit; only round corners */
    div[data-testid="stNotification"], .stAlert {
        border-radius: 10px !important;
    }

    .card {
        background: var(--bg-page);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem 1.35rem;
        text-align: left;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    }
    .card h3 {
        margin: 0 0 0.75rem 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
    }
    .card p {
        margin: 0;
        color: var(--text-soft);
        line-height: 1.6;
        font-size: 0.95rem;
        white-space: pre-wrap;
    }
</style>
"""

st.markdown(
    _THEME_STYLE_REST.replace("___ROOT_VARS___", _ROOT_DARK if _IS_DARK else _ROOT_LIGHT).replace(
        "___CONTAINER_BG___", _CONTAINER_DARK if _IS_DARK else _CONTAINER_LIGHT
    ),
    unsafe_allow_html=True,
)

# -------------------------------
# Hero
# -------------------------------
st.markdown(
    """
<div class="app-hero">
    <div class="app-hero-badge">Operations</div>
    <h1>Energy forecast dashboard</h1>
    <p>Hourly load inputs, forecast output, and optimization guidance for grid operations teams.</p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "energy_values" not in st.session_state:
    st.session_state.energy_values = [14000.0] * 24

for i in range(24):
    if f"input_{i}" not in st.session_state:
        st.session_state[f"input_{i}"] = st.session_state.energy_values[i]

# -------------------------------
# DATA INPUT
# -------------------------------
st.markdown('<p class="section-label">Data input</p>', unsafe_allow_html=True)

colA, colB = st.columns([1, 2])

with colA:
    if st.button("Load sample series", use_container_width=True):
        new_vals = list(np.linspace(14000, 15500, 24))
        st.session_state.energy_values = new_vals
        for i in range(24):
            st.session_state[f"input_{i}"] = new_vals[i]

with colB:
    file = st.file_uploader("Upload hourly CSV", type=["csv"], label_visibility="visible")

if file:
    df_upload = pd.read_csv(file)
    st.success("CSV loaded.")

    numeric_cols = df_upload.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        st.error("No numeric columns found in this file.")
    else:
        selected_column = st.selectbox("Energy column", numeric_cols)

        new_values = df_upload[selected_column].dropna().tolist()[:24]

        if len(new_values) < 24:
            st.warning("Provide at least 24 numeric values.")
        else:
            st.session_state.energy_values = new_values
            for i in range(24):
                st.session_state[f"input_{i}"] = new_values[i]

# -------------------------------
# INPUT GRID
# -------------------------------
st.markdown('<p class="section-label">Hourly energy (MW) — 24 hours</p>', unsafe_allow_html=True)

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

# -------------------------------
# CHART
# -------------------------------
st.markdown('<p class="section-label">Load profile</p>', unsafe_allow_html=True)

mpl.rcParams["font.family"] = ["DM Sans", "DejaVu Sans", "sans-serif"]
if _IS_DARK:
    chart_bg = "#0d1117"
    plot_fill = "#161b22"
    accent = "#818cf8"
    accent_soft = "#a5b4fc"
    grid_c = "#30363d"
    label_c = "#e6edf3"
    spine_c = "#484f58"
else:
    chart_bg = "#ffffff"
    plot_fill = "#f8fafc"
    accent = "#4f46e5"
    accent_soft = "#6366f1"
    grid_c = "#e2e8f0"
    label_c = "#0f172a"
    spine_c = "#334155"

_pt_face = "#ffffff" if not _IS_DARK else "#21262d"

fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=chart_bg)
ax.set_facecolor(plot_fill)
ax.fill_between(range(1, 25), values, alpha=0.12, color=accent, zorder=1)
ax.plot(
    range(1, 25),
    values,
    color=accent,
    linewidth=2.5,
    marker="o",
    markersize=5,
    markerfacecolor=_pt_face,
    markeredgecolor=accent_soft,
    markeredgewidth=2,
    zorder=2,
)
ax.set_xlabel("Hour", color=label_c, fontsize=10, fontweight=500)
ax.set_ylabel("Energy (MW)", color=label_c, fontsize=10, fontweight=500)
ax.set_xticks(range(1, 25, 2))
ax.tick_params(axis="both", colors=label_c, labelsize=9)
ax.grid(True, axis="y", linestyle="-", alpha=0.85, color=grid_c, linewidth=0.8)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_color(spine_c)
    spine.set_linewidth(1)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# -------------------------------
# APPLIANCE INPUTS (sent with optimize → Groq)
# -------------------------------
st.markdown('<p class="section-label">Appliance usage (kWh)</p>', unsafe_allow_html=True)
st.caption("Typical period totals for your home — used for AI analysis when you run optimization.")

ap1, ap2 = st.columns(2)
with ap1:
    appliances = {
        "AC": st.number_input("AC (kWh)", min_value=0.0, value=2.0, step=0.1, format="%.2f", key="appl_ac"),
        "Refrigerator": st.number_input(
            "Refrigerator (kWh)", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="appl_fridge"
        ),
        "Washing Machine": st.number_input(
            "Washing Machine (kWh)", min_value=0.0, value=0.5, step=0.1, format="%.2f", key="appl_wm"
        ),
        "Lights": st.number_input("Lights (kWh)", min_value=0.0, value=0.8, step=0.1, format="%.2f", key="appl_lights"),
    }
with ap2:
    appliances.update(
        {
            "Fans": st.number_input("Fans (kWh)", min_value=0.0, value=0.6, step=0.1, format="%.2f", key="appl_fans"),
            "TV": st.number_input("TV (kWh)", min_value=0.0, value=0.4, step=0.1, format="%.2f", key="appl_tv"),
            "Laptop": st.number_input("Laptop (kWh)", min_value=0.0, value=0.3, step=0.1, format="%.2f", key="appl_laptop"),
            "Others": st.number_input("Others (kWh)", min_value=0.0, value=0.5, step=0.1, format="%.2f", key="appl_others"),
        }
    )

# -------------------------------
# ACTIONS
# -------------------------------
st.markdown('<p class="section-label">Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

prediction = None
status = None
suggestion = None
ai_suggestion = None

with col1:
    if st.button("Generate forecast", use_container_width=True):
        try:
            res = requests.post(
                f"{API_URL}/predict",
                json={"input": values},
                timeout=60,
            )
            res.raise_for_status()
            prediction = res.json()["prediction_MW"]
        except Exception:
            st.error("Could not reach the forecast service.")

with col2:
    if st.button("Run optimization", use_container_width=True):
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
        except Exception:
            st.error("Could not reach the forecast service.")

# -------------------------------
# KPI CARDS
# -------------------------------
if prediction:

    def _status_class(s: str) -> str:
        if not s:
            return "value-yellow"
        s_lower = s.lower()
        if "low" in s_lower:
            return "value-green"
        if "moderate" in s_lower:
            return "value-yellow"
        return "value-red"

    c1 = f'<div class="kpi-card"><h4>Forecast output</h4><p class="value-green">{prediction:.2f} MW</p></div>'

    c2 = ""
    if status:
        sc = _status_class(status)
        c2 = f'<div class="kpi-card"><h4>Utilization</h4><p class="{sc}">{status}</p></div>'

    c3 = ""
    if suggestion:
        esc = (
            suggestion.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        c3 = f'<div class="kpi-card"><h4>Recommendation</h4><p class="body-text">{esc}</p></div>'

    st.markdown(
        f'<div class="kpi-grid">{c1}{c2}{c3}</div>',
        unsafe_allow_html=True,
    )

if ai_suggestion is not None and str(ai_suggestion).strip():
    st.markdown('<p class="section-label">AI smart suggestions</p>', unsafe_allow_html=True)
    body_esc = html.escape(str(ai_suggestion)).replace("\n", "<br/>")
    st.markdown(
        f"""
    <div class="card">
        <h3>AI analysis</h3>
        <p>{body_esc}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# -------------------------------
# HISTORY
# -------------------------------
st.markdown('<p class="section-label">History</p>', unsafe_allow_html=True)

if st.button("Refresh history", use_container_width=True):
    try:
        res = requests.get(f"{API_URL}/history", timeout=30)
        res.raise_for_status()
        data = res.json()

        if len(data) == 0:
            st.info("No saved forecasts yet.")
        else:
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    except Exception:
        st.error("Could not load history from the API.")
