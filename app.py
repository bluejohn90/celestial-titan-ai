import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Celestial Titan AI v2", layout="wide")

# 🚀 Cache system for speed
@st.cache_data
def load_csv(uploaded, sample_str):
    """Load CSV with caching to speed up reloads"""
    return pd.read_csv(uploaded) if uploaded else pd.read_csv(StringIO(sample_str))

@st.cache_resource
def get_base_df():
    """Keep base DataFrame in memory between reruns"""
    return pd.DataFrame()

# 🛰️ Rarity Radar (Triples / Quads / Quints)
label = "Triples / Quads / Quints Radar"
with st.expander(label, expanded=False):
    st.caption("Tip: larger 'gap' = mas matagal nang di lumalabas sa history window.")
    st.dataframe(
        pd.DataFrame({
            "digit": [1,2,3,4,5],
            "combo": ["1111","2222","3333","4444","5555"],
            "gap": [10,20,15,5,8],
            "seen": [True, False, True, True, False]
        }),
        use_container_width=True,
        height=220
    )
