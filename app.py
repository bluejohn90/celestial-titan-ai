# Celestial Titan AI — Optimized Ensemble (Pick3/4/5)
import streamlit as st, pandas as pd, numpy as np
from io import StringIO
from itertools import product
st.set_page_config(page_title="Celestial Titan AI", layout="wide")
st.title("🌌 Celestial Titan AI — Optimized Ensemble")
st.caption("Pick 3 • Pick 4 • Pick 5 — frequency + mirrors + sum-bands + position distributions")

MIRROR = {0:5,1:6,2:7,3:8,4:9,5:0,6:1,7:2,8:3,9:4}

def load_csv(uploaded, sample_str):
    return pd.read_csv(uploaded) if uploaded else pd.read_csv(StringIO(sample_str))

def validate_df(df, n):
    need = [f"d{i+1}" for i in range(n)]
    for c in need:
        if c not in df.columns: raise ValueError(f"Missing column: {c}")
        df[c] = df[c].astype(int)
        if df[c].min()<0 or df[c].max()>9: raise ValueError(f"{c} must be 0–9")
    return df.dropna(subset=need)

def features(df, n):
    digits = list(range(10))
    pos = {i: df[f"d{i+1}"].value_counts().reindex(digits, fill_value=0).to_numpy() for i in range(n)}
    posn = {i: v/(v.sum()+1e-9) for i,v in pos.items()}
    overall = np.sum([pos[i] for i in range(n)], axis=0); overalln = overall/(overall.sum()+1e-9)
    sums = np.zeros(len(df), dtype=int)
    for i in range(n): sums += df[f"d{i+1}"].to_numpy()
    summax = 9*n; sc = np.zeros(summax+1)
    for s in sums: sc[int(s)] += 1
    sumn = sc/(sc.sum()+1e-9)
    def rep(r): v=[int(r[f"d{i+1}"]) for i in range(n)]; return int(len(set(v))<len(v))
    dblr = df.apply(rep, axis=1).mean()
    return posn, overalln, sumn, dblr

def score(digs, posn, overalln, sumn, dblr, W):
    wf, wm, ws, wp, wd = W; n=len(digs)
    fpos = np.mean([posn[i][digs[i]] for i in range(n)])
    fov  = np.mean([overalln[d] for d in digs]); s_freq = 0.5*fpos+0.5*fov
    hot = np.argsort(-overalln)[:5]; hotm = {MIRROR[int(d)] for d in hot}
    s_mirr = sum(d in hotm for d in digs)/n
    s_sum = sumn[sum(digs)]
    s_pos = fpos
    s_dbl = 1.0 if len(set(digs))<n else (0.5 if dblr<0.25 else 0.0)
    return wf*s_freq + wm*s_mirr + ws*s_sum + wp*s_pos + wd*s_dbl

def generate(df, n, hotk, warmk, maxc, topn, W):
    posn, overalln, sumn, dblr = features(df, n)
    order = np.argsort(-overalln); hot = order[:hotk].tolist(); warm = order[hotk:hotk+warmk].tolist()
    cand = sorted(set(hot + warm + [MIRROR[d] for d in hot]))
    pool = list(product(cand, repeat=n))[:maxc]
    scored = [("".join(map(str,x)), float(score(x,posn,overalln,sumn,dblr,W))) for x in pool]
    scored.sort(key=lambda t:t[1], reverse=True)
    return pd.DataFrame(scored[:topn], columns=["combo","score"]), cand

def ui_tab(label, n, sample):
    st.subheader(f"{label} (Pick {n})")
    up = st.file_uploader(f"Upload CSV for Pick {n} (optional)", type=["csv"], key=f"u{n}")
    df = validate_df(load_csv(up, sample), n)
    c1,c2,c3,c4 = st.columns(4)
    with c1: win = st.slider("History window", 20, min(1000,len(df)), min(300,len(df)))
    dfw = df.tail(win)
    with c2: hotk = st.slider("Hot digits", 3, 7, 5); warmk = st.slider("Warm digits", 0, 6, 3)
    with c3: maxc = st.slider("Max candidates", 100, 5000, 1024, 64)
    with c4: topn = st.slider("Show top N", 5, 100, 20)
    w1,w2,w3,w4,w5 = st.columns(5)
    wf=w1.slider("Freq",0.0,1.0,0.35,0.05,key=f"wf{n}")
    wm=w2.slider("Mirror",0.0,1.0,0.20,0.05,key=f"wm{n}")
    ws=w3.slider("Sum",0.0,1.0,0.20,0.05,key=f"ws{n}")
    wp=w4.slider("Position",0.0,1.0,0.15,0.05,key=f"wp{n}")
    wd=w5.slider("Doubles",0.0,1.0,0.10,0.05,key=f"wd{n}")
    W = np.array([wf,wm,ws,wp,wd]); W = W/(W.sum()+1e-9)
    out, cand = generate(dfw, n, hotk, warmk, int(maxc), int(topn), W)
    l,r = st.columns([2,1])
    with l:
        st.write(f"**Candidate digits:** {cand}")
        st.dataframe(out,
# --- Rarity Radar (triples/quads/quints) ---
label = {3:"Triples Radar", 4:"Quad Radar", 5:"Quints Radar"}[n]
with st.expander(f"🛰️ {label}", expanded=False):
    stats = rarity_gaps(dfw, n)
    st.caption("Tip: larger 'gap' = mas matagal nang di lumalabas sa history window.")
    st.dataframe(
        pd.DataFrame(stats)[["digit","combo","gap","seen"]],
        use_container_width=True, height=220
    )
    if st.button(f"Add top 3 {('triples' if n==3 else 'quads' if n==4 else 'quints')} to candidates", key=f"add_rarity_{n}"):
        rare_combos = ["".join(c) if isinstance(c, tuple) else c for c in [s["combo"] for s in stats[:3]]]
        # prepend to the scored output (with a slight score boost so they appear at the top)
        boost = pd.DataFrame({"combo": rare_combos, "score": [1.0]*len(rare_combos)})
        out = pd.concat([boost, out[~out["combo"].isin(rare_combos)]], ignore_index=True)
use_container_width=True, height=420)
        st.download_button("⬇️ Download Top (CSV)", out.to_csv(index=False).encode(), file_name=f"celestial_pick{n}.csv", mime="text/csv")
        st.download_button("⬇️ Download Top (TXT)", "\n".join(out['combo']).encode(), file_name=f"celestial_pick{n}.txt", mime="text/plain")
    with r:
        if len(out):
            top = out.iloc[0]["combo"]; from itertools import permutations
            box = sorted({"".join(p) for p in permutations(list(top), n)})
            st.markdown(f"**Top pick:** `{top}`")
            st.markdown("**Box cover:** " + ", ".join(box))

SAMPLE_P3 = '''draw_date,draw,d1,d2,d3
2025-10-20,3-0-4,3,0,4
2025-10-19,3-5-9,3,5,9
2025-10-18,6-3-9,6,3,9
2025-10-17,2-6-4,2,6,4
2025-10-16,4-0-2,4,0,2
2025-10-15,7-7-1,7,7,1
2025-10-14,5-1-5,5,1,5
2025-10-13,1-8-3,1,8,3
2025-10-12,9-2-8,9,2,8
2025-10-11,6-4-0,6,4,0
'''
SAMPLE_P4 = '''draw_date,draw,d1,d2,d3,d4
2025-10-20,3-0-4-2,3,0,4,2
2025-10-19,7-7-4-1,7,7,4,1
2025-10-18,9-0-3-6,9,0,3,6
2025-10-17,5-1-8-0,5,1,8,0
2025-10-16,2-2-4-6,2,2,4,6
2025-10-15,1-9-4-0,1,9,4,0
2025-10-14,3-7-8-0,3,7,8,0
2025-10-13,0-6-3-4,0,6,3,4
2025-10-12,2-4-6-8,2,4,6,8
2025-10-11,8-1-1-5,8,1,1,5
'''
SAMPLE_P5 = '''draw_date,draw,d1,d2,d3,d4,d5
2025-10-20,4-8-6-0-4,4,8,6,0,4
2025-10-19,7-3-5-9-3,7,3,5,9,3
2025-10-18,6-3-9-1-4,6,3,9,1,4
2025-10-17,2-6-4-0-2,2,6,4,0,2
2025-10-16,4-0-2-7-9,4,0,2,7,9
2025-10-15,7-7-1-4-1,7,7,1,4,1
2025-10-14,5-1-8-0-5,5,1,8,0,5
2025-10-13,1-8-3-2-4,1,8,3,2,4
2025-10-12,9-2-8-7-1,9,2,8,7,1
2025-10-11,6-4-0-3-6,6,4,0,3,6
'''

tab3, tab4, tab5 = st.tabs(["Pick 3", "Pick 4", "Pick 5"])
with tab3: ui_tab("Pick 3", 3, SAMPLE_P3)
with tab4: ui_tab("Pick 4", 4, SAMPLE_P4)
with tab5: ui_tab("Pick 5", 5, SAMPLE_P5)
st.info("Tip: Upload 180–300 recent draws per game for better signals. Adjust weights per state profile.")

# ---- RARITY RADAR HELPERS ----
def rarity_gaps(df, n):
    """Return gap stats for same-digit runs (triples/quads/quints)."""
    # rows are chronological; we traverse from newest to oldest
    m = {}  # digit -> gap (0 = just hit)
    total = len(df)
    for d in range(10):
        m[d] = None  # None = never seen in history

    # scan newest->oldest
    for idx, (_, row) in enumerate(reversed(df.reset_index(drop=True)).iterrows()):
        digs = [int(row[f"d{i+1}"]) for i in range(n)]
        if len(set(digs)) == 1:
            d = digs[0]
            if m[d] is None:
                m[d] = idx  # first time we encounter from newest side

    # convert None to a big gap (=total draws)
    out = []
    for d in range(10):
        gap = m[d] if m[d] is not None else total
        out.append({"digit": d, "combo": str(d)*n, "gap": int(gap), "seen": m[d] is not None})
    out.sort(key=lambda x: (-x["gap"], x["digit"]))
    return out
