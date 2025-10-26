# app.py
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

# --- Page config and global style ---
st.set_page_config(
    page_title="🎯 Celestial Titan AI Pro v2",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global dark theme CSS ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #0B0B20;
            color: white;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #101020;
        }
        h1, h2, h3, h4, h5, h6, p, div, span, a {
            color: #E0E0E0 !important;
        }
        .card {
            background-color: rgba(255,255,255,0.03);
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        @media (max-width: 600px) {
            .card { padding: 12px; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar controls ---
with st.sidebar:
    st.title("Celestial Titan AI 🌌")
    st.markdown("### Quad Sniper Analyzer")
    uploaded_file = st.file_uploader(
        "Upload results CSV or Excel file",
        type=["csv", "xlsx"],
        help="Upload a file with columns: date, draw_time, numbers"
    )
    st.markdown("---")
    st.markdown("**Settings**")
    preset = st.selectbox("Preset", ["A", "B", "Custom"])
    run_analysis = st.button("Run Analysis")

# --- Main layout ---
st.header("🎯 Quad Sniper Analyzer")
st.markdown("Analyze Pick-3/4/5 results, generate candidate sets, and export them easily.")

col1, col2 = st.columns([2, 1])

# --- Input / Preview section ---
with col1:
    st.subheader("Input / Preview")
    df = None

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.markdown("**Preview of uploaded data**")
            st.dataframe(df.head(50))
        except Exception as e:
            st.error(f"Unable to read file: {e}")
    else:
        st.info("No file uploaded. You can use the sample dataset below.")
        if st.button("Use sample dataset"):
            df = pd.DataFrame({
                "date": pd.date_range(end=pd.Timestamp.today(), periods=10).strftime("%Y-%m-%d"),
                "draw_time": ["Evening"]*10,
                "numbers": ["12345","67890","11223","44556","77889","00999","33011","77444","55667","88900"]
            })
            st.session_state["sample_df"] = df
            st.experimental_rerun()

with col2:
    st.subheader("Quick Settings")
    st.markdown("Use the sliders to fine-tune your analysis.")

    # ✅ Safe slider (auto min/max)
    if "sample_df" in st.session_state:
        df_len = len(st.session_state["sample_df"])
    elif df is not None:
        df_len = len(df)
    else:
        df_len = 10  # fallback

    min_val = 1
    max_val = max(10, df_len)
    default_val = min(max_val // 2, 10)
    st.slider("History window", min_val, max_val, default_val)

# --- Analysis section ---
st.markdown("## 🔍 Analysis")
if run_analysis:
    st.markdown("### Running analysis...")
    try:
        # pick the dataframe
        if df is None and "sample_df" in st.session_state:
            df_to_use = st.session_state["sample_df"]
        else:
            df_to_use = df

        if df_to_use is None:
            st.warning("No data available to analyze.")
        else:
            # simple example: digit frequency
            all_digits = "".join(df_to_use["numbers"].astype(str).tolist())
            digit_counts = {str(i): all_digits.count(str(i)) for i in range(10)}
            freq_df = pd.DataFrame(list(digit_counts.items()), columns=["digit","count"]).sort_values("count", ascending=False)
            st.table(freq_df)

            st.success("✅ Analysis complete. See candidate sets below.")

            # simple random generator placeholder
            candidates = []
            for _ in range(10):
                candidate = "".join(np.random.choice(list("0123456789"), size=5))
                candidates.append(candidate)

            st.markdown("**Candidate Sets (Example)**")
            st.write(candidates)
    except Exception as e:
        st.error(f"Error during analysis: {e}")

# --- Export / Save section ---
st.markdown("---")
st.markdown("### 💾 Export")
if st.button("Export candidates to CSV"):
    try:
        cand_df = pd.DataFrame({"candidate": ["00000","11111"]})
        csv = cand_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="candidates.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Export failed: {e}")

# --- Footer ---
st.markdown(
    """
    <div style="opacity:0.7; font-size:12px; margin-top:20px;">
    Made with ❤️ — Celestial Titan AI Pro v2<br>
    Kaibigan, sabihin mo kung gusto mong i-integrate agad ang Quad Sniper logic (optimizer settings, 5-star filter, SD thresholds, etc.)
    </div>
    """,
    unsafe_allow_html=True
)
