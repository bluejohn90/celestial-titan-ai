# app.py — Celestial Titan AI Pro v2

import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

# ---------------- Page config ----------------
st.set_page_config(
    page_title="🎯 Celestial Titan AI Pro v2",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Global CSS (dark) ----------------
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { background-color: #0B0B20; color: white; }
        [data-testid="stAppViewContainer"] { background-color: #101020; }
        h1,h2,h3,h4,h5,h6,p,div,span,a { color: #E0E0E0 !important; }
        .card { background-color: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; margin-bottom:12px; }
        @media (max-width: 600px) { .card { padding: 10px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Helper: safe slider ----------------
def safe_slider(label: str, df_like=None, requested_min=1, requested_default=None):
    """
    Safe slider wrapper (prevents min==max errors).
    """
    try:
        if isinstance(df_like, (pd.DataFrame, list, tuple, str)):
            length = len(df_like)
        elif isinstance(df_like, int):
            length = df_like
        else:
            length = 0

        if length <= 1:
            length = 10
        min_val = max(1, requested_min)
        max_val = max(min_val + 1, length)
        if requested_default is None:
            default_val = min(max_val // 2, 10)
        else:
            default_val = max(min_val, min(requested_default, max_val))
        return st.slider(label, min_val, max_val, default_val)
    except Exception:
        return st.slider(label, 1, 10, 5)

# ---------------- Sidebar controls ----------------
with st.sidebar:
    st.title("🌌 Celestial Titan AI Pro v2")
    st.markdown("### Quad Sniper Analyzer")
    uploaded_file = st.file_uploader(
        "Upload results CSV or Excel (columns: date, draw_time, numbers)",
        type=["csv", "xlsx"],
    )
    st.markdown("---")
    st.markdown("**Settings**")
    preset = st.selectbox("Preset", ["A", "B", "Custom"])
    run_analysis = st.button("Run Analysis")

# ---------------- Main Header ----------------
st.header("🎯 Quad Sniper Analyzer")
st.markdown("Analyze Pick-3/4/5 results, generate candidate sets, and export them.")

# ---------------- Tabs (Pick 3 / Pick 4 / Pick 5) ----------------
tab1, tab2, tab3 = st.tabs(["Pick 3", "Pick 4", "Pick 5"])

# ---------------- Function: Load or Sample Data ----------------
def load_dataset(uploaded_file):
    df = None
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
            else:
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file)
            st.success("✅ File loaded successfully.")
        except Exception as e:
            st.error(f"Unable to read file: {e}")
            df = None
    else:
        st.info("No file uploaded. You can paste CSV text or use the sample dataset below.")
        sample_text = st.text_area("Paste CSV text (optional)", height=120)
        if sample_text:
            try:
                df = pd.read_csv(StringIO(sample_text))
                st.success("✅ Loaded pasted CSV text.")
            except Exception as e:
                st.error(f"Couldn't parse pasted CSV text: {e}")
        if st.button("Use sample dataset"):
            df = pd.DataFrame({
                "date": pd.date_range(end=pd.Timestamp.today(), periods=10).strftime("%Y-%m-%d"),
                "draw_time": ["Evening"]*10,
                "numbers": ["12345","67890","11223","44556","77889","00999","33011","77444","55667","88900"]
            })
            st.session_state["sample_df"] = df
            st.experimental_rerun()
    return df

# ---------------- Function: Run Analysis ----------------
def analyze_dataset(df, n_digits):
    if df is None or "numbers" not in df.columns:
        st.warning("Please load a valid dataset with a 'numbers' column.")
        return
    st.markdown("#### 🔍 Digit Frequency Analysis")
    all_digits = "".join(df["numbers"].astype(str).tolist())
    digit_counts = {str(i): all_digits.count(str(i)) for i in range(10)}
    freq_df = pd.DataFrame(list(digit_counts.items()), columns=["Digit", "Count"]).sort_values("Count", ascending=False)
    st.table(freq_df)

    st.markdown("#### 🎯 Candidate Sets (sample generator)")
    candidates = ["".join(np.random.choice(list("0123456789"), size=n_digits)) for _ in range(10)]
    st.write(candidates)

# ---------------- TAB: Pick 3 ----------------
with tab1:
    st.subheader("🎲 Pick 3 Analyzer")
    df3 = load_dataset(uploaded_file)
    if df3 is not None:
        st.dataframe(df3.head(20))
    st.markdown("---")
    history_window = safe_slider("History window", df3)
    st.text(f"Using history window = {history_window}")
    if run_analysis:
        analyze_dataset(df3, 3)

# ---------------- TAB: Pick 4 ----------------
with tab2:
    st.subheader("🎲 Pick 4 Analyzer")
    df4 = load_dataset(uploaded_file)
    if df4 is not None:
        st.dataframe(df4.head(20))
    st.markdown("---")
    history_window = safe_slider("History window", df4)
    st.text(f"Using history window = {history_window}")
    if run_analysis:
        analyze_dataset(df4, 4)

# ---------------- TAB: Pick 5 ----------------
with tab3:
    st.subheader("🎲 Pick 5 Analyzer")
    df5 = load_dataset(uploaded_file)
    if df5 is not None:
        st.dataframe(df5.head(20))
    st.markdown("---")
    history_window = safe_slider("History window", df5)
    st.text(f"Using history window = {history_window}")
    if run_analysis:
        analyze_dataset(df5, 5)

# ---------------- Export ----------------
st.markdown("---")
st.markdown("### 💾 Export Candidates")
if st.button("Export candidates to CSV"):
    try:
        cand_df = pd.DataFrame({"candidate": ["00000","11111","22222","33333","44444"]})
        csv = cand_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="candidates.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Export failed: {e}")

# ---------------- Footer ----------------
st.markdown(
    """
    <div style="opacity:0.8; font-size:12px; margin-top:16px;">
    Made with ❤️ — Celestial Titan AI Pro v2<br>
    Tip: upload a CSV with a column named <code>numbers</code> (e.g. "12345") for analysis.
    </div>
    """,
    unsafe_allow_html=True,
)
