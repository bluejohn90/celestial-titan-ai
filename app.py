# app.py
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
    A safe slider wrapper that never raises StreamlitAPIException about min/max.
    - df_like: object with length (e.g., pd.DataFrame) or an integer number of rows.
    - requested_min: base min value (default 1).
    - requested_default: optional default value; if None we pick a reasonable default.
    Returns the selected int (but we don't rely on the return value in this template).
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
        max_val = max(10, length)
        if requested_default is None:
            default_val = min(max_val // 2, 10)
        else:
            default_val = requested_default
            # clamp default
            default_val = max(min_val, min(default_val, max_val))
        return st.slider(label, min_val, max_val, default_val)
    except Exception:
        # worst-case fallback (guaranteed valid)
        return st.slider(label, 1, 10, 5)


# ---------------- Sidebar controls ----------------
with st.sidebar:
    st.title("Celestial Titan AI 🌌")
    st.markdown("### Quad Sniper Analyzer")
    uploaded_file = st.file_uploader(
        "Upload results CSV or Excel file (columns: date, draw_time, numbers)",
        type=["csv", "xlsx"],
    )
    st.markdown("---")
    st.markdown("**Settings**")
    preset = st.selectbox("Preset", ["A", "B", "Custom"])
    run_analysis = st.button("Run Analysis")

# ---------------- Main UI ----------------
st.header("🎯 Quad Sniper Analyzer")
st.markdown("Analyze Pick-3/4/5 results, generate candidate sets, and export them.")

col1, col2 = st.columns([2, 1])

# --- Input / Preview (left) ---
with col1:
    st.subheader("Input / Preview")
    df = None

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                # try reading csv (handle text uploads)
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
            else:
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file)
            st.markdown("**Preview of uploaded data**")
            st.dataframe(df.head(50))
        except Exception as e:
            st.error(f"Unable to read file: {e}")
            df = None
    else:
        st.info("No file uploaded. Use the sample dataset or paste CSV text.")
        sample_text = st.text_area("Paste CSV text (optional)", height=120)
        if sample_text:
            try:
                df = pd.read_csv(StringIO(sample_text))
                st.success("Loaded pasted CSV text.")
                st.dataframe(df.head(50))
            except Exception as e:
                st.error(f"Couldn't parse pasted CSV text: {e}")
                df = None

        if st.button("Use sample dataset"):
            df = pd.DataFrame({
                "date": pd.date_range(end=pd.Timestamp.today(), periods=10).strftime("%Y-%m-%d"),
                "draw_time": ["Evening"]*10,
                # sample numbers (as strings) for pick-5 style
                "numbers": ["12345","67890","11223","44556","77889","00999","33011","77444","55667","88900"]
            })
            st.session_state["sample_df"] = df
            st.experimental_rerun()

# --- Quick Controls (right) ---
with col2:
    st.subheader("Quick Controls")
    st.markdown("Adjust the analysis window and quick settings.")
    # choose df source for slider information
    df_for_slider = None
    if df is not None:
        df_for_slider = df
    elif "sample_df" in st.session_state:
        df_for_slider = st.session_state["sample_df"]
    else:
        df_for_slider = 10

    # Use safe slider wrapper
    history_window = safe_slider("History window", df_for_slider)
    st.text(f"Using history window = {history_window}")

    # extra quick toggles (example)
    st.checkbox("Enable advanced candidate filter (placeholder)", value=False)
    st.selectbox("Candidate length", [3, 4, 5], index=2)

# ---------------- Analysis ----------------
st.markdown("## 🔍 Analysis")
if run_analysis:
    st.markdown("### Running analysis...")
    try:
        # prioritize uploaded / pasted / sample
        if df is None and "sample_df" in st.session_state:
            df_to_use = st.session_state["sample_df"]
        else:
            df_to_use = df

        if df_to_use is None:
            st.warning("No data available to analyze. Upload CSV or use the sample dataset.")
        else:
            # Basic validation for 'numbers' column
            if "numbers" not in df_to_use.columns:
                st.error("The dataframe must contain a 'numbers' column (strings like 12345).")
            else:
                # Example analysis: digit frequency across all entries
                all_digits = "".join(df_to_use["numbers"].astype(str).tolist())
                digit_counts = {str(i): all_digits.count(str(i)) for i in range(10)}
                freq_df = pd.DataFrame(list(digit_counts.items()), columns=["digit", "count"]).sort_values("count", ascending=False)
                st.markdown("#### Digit frequency (example)")
                st.table(freq_df)

                st.success("✅ Analysis complete.")

                # Placeholder candidate generator (random)
                candidate_len = 5  # example - you can make this dynamic via UI
                candidates = ["".join(np.random.choice(list("0123456789"), size=candidate_len)) for _ in range(10)]
                st.markdown("**Candidate sets (example)**")
                st.write(candidates)

    except Exception as e:
        st.error(f"Error during analysis: {e}")

# ---------------- Export ----------------
st.markdown("---")
st.markdown("### 💾 Export")
if st.button("Export candidates to CSV"):
    try:
        cand_df = pd.DataFrame({"candidate": ["00000","11111"]})
        csv = cand_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="candidates.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Export failed: {e}")

# ---------------- Footer ----------------
st.markdown(
    """
    <div style="opacity:0.8; font-size:12px; margin-top:16px;">
    Made with ❤️ — Celestial Titan AI Pro v2<br>
    Tip: upload a CSV with a column named <code>numbers</code> (strings like "12345") for the sample analysis to work.
    </div>
    """,
    unsafe_allow_html=True
)
