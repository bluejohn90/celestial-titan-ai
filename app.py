import streamlit as st
import json
import random
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Celestial Titan God AI",
    page_icon="🌀",
    layout="wide"
)

# ===============================
# TITAN THEME
# ===============================
PRIMARY = "#00C6FF"
SECONDARY = "#8F00FF"
BACKGROUND = "#050B1A"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {BACKGROUND};
        color: white;
    }}
    .stApp {{
        background: radial-gradient(circle at top, #0a1a3a, #020617);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# HEADER
# ===============================
st.markdown(
    """
    <h1 style="text-align:center; color:#7dd3fc;">
        🌌 Celestial Titan God AI
    </h1>
    <p style="text-align:center; color:#cbd5f5;">
        Cosmic Lottery Intelligence • Prototype Core Activated
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("🧠 Titan Control Panel")
mode = st.sidebar.radio(
    "Select Mode",
    [
        "Daily Forecast",
        "Random Cosmic Draw",
        "Titan Status"
    ]
)

# ===============================
# MODES
# ===============================
if mode == "Daily Forecast":
    st.subheader("🎯 Daily Titan Forecast")

    numbers = sorted(random.sample(range(0, 10), 3))
    st.markdown(
        f"""
        <div style="font-size:28px; color:#38bdf8;">
            Titan suggests: <b>{numbers}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

elif mode == "Random Cosmic Draw":
    st.subheader("🌠 Cosmic Randomizer")

    count = st.slider("How many numbers?", 3, 6, 3)
    result = sorted(random.sample(range(0, 10), count))

    st.success(f"Cosmic Output: {result}")

elif mode == "Titan Status":
    st.subheader("⚙️ Titan System Status")

    st.json(
        {
            "Titan Core": "ONLINE",
            "Version": "Nano Core v60.7.6 (Streamlit Cloud)",
            "Data Engine": "Not yet attached",
            "Accuracy Engine": "Dormant",
            "Last Sync": datetime.now().isoformat()
        }
    )

# ===============================
# FOOTER
# ===============================
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:#64748b;">
        © 2025 Celestial Titan God AI • Streamlit Cloud Prototype
    </p>
    """,
    unsafe_allow_html=True
)
