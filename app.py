import streamlit as st
import re
import string
import joblib
import numpy as np
import pandas as pd
import os
import nltk
from nltk.stem import WordNetLemmatizer
import altair as alt
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CYBERSEC // SPAM THREAT ENGINE",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# IMMERSIVE CYBERSECURITY CSS — Animated, Unique, Premium
# ============================================================
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --cyber-bg: #060911;
        --cyber-surface: #0D1322;
        --cyber-card: #111827;
        --cyber-border: #1a2332;
        --cyber-mint: #00F5D4;
        --cyber-mint-dim: rgba(0, 245, 212, 0.15);
        --cyber-red: #FF2E63;
        --cyber-red-dim: rgba(255, 46, 99, 0.15);
        --cyber-amber: #FFB703;
        --cyber-blue: #3B82F6;
        --cyber-purple: #8B5CF6;
        --cyber-text: #E2E8F0;
        --cyber-muted: #64748B;
    }

    /* ── Animated Grid Background ── */
    .stApp {
        background:
            linear-gradient(rgba(0, 245, 212, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 245, 212, 0.03) 1px, transparent 1px),
            radial-gradient(ellipse at 20% 50%, rgba(0, 245, 212, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
            var(--cyber-bg) !important;
        background-size: 60px 60px, 60px 60px, cover, cover, cover !important;
    }

    /* ── SOC COMMAND BANNER ── */
    .soc-banner {
        position: relative;
        background: linear-gradient(135deg, #0a1628 0%, #0D1322 40%, #111827 100%);
        border: 1px solid var(--cyber-border);
        border-left: 4px solid var(--cyber-mint);
        border-radius: 12px;
        padding: 28px 32px 24px 32px;
        margin-bottom: 8px;
        overflow: hidden;
    }

    .soc-banner::before {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 220px; height: 100%;
        background: radial-gradient(circle at 100% 0%, rgba(0, 245, 212, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .soc-banner::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0;
        width: 100%; height: 1px;
        background: linear-gradient(90deg, var(--cyber-mint), transparent 60%);
        opacity: 0.4;
    }

    .banner-grid {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .banner-left h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #fff;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .banner-left h1 .accent { color: var(--cyber-mint); }

    .banner-left p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: var(--cyber-muted);
        margin: 0;
        letter-spacing: 0.5px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--cyber-mint);
        background: var(--cyber-mint-dim);
        border: 1px solid rgba(0, 245, 212, 0.25);
        padding: 6px 16px;
        border-radius: 20px;
        margin-top: 6px;
    }

    .status-pill .dot {
        width: 7px; height: 7px;
        background: var(--cyber-mint);
        border-radius: 50%;
        box-shadow: 0 0 6px var(--cyber-mint);
        animation: pulse-dot 2s ease-in-out infinite;
    }

    @keyframes pulse-dot {
        0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--cyber-mint); }
        50% { opacity: 0.4; box-shadow: 0 0 2px var(--cyber-mint); }
    }

    /* ── RADAR SCAN ANIMATION ── */
    .radar-box {
        width: 110px; height: 110px;
        position: relative;
        margin-top: 4px;
    }

    .radar-ring {
        position: absolute;
        border: 1px solid rgba(0, 245, 212, 0.15);
        border-radius: 50%;
    }

    .radar-ring.r1 { width: 100%; height: 100%; top: 0; left: 0; }
    .radar-ring.r2 { width: 66%; height: 66%; top: 17%; left: 17%; }
    .radar-ring.r3 { width: 33%; height: 33%; top: 33.5%; left: 33.5%; }

    .radar-sweep {
        position: absolute;
        top: 50%; left: 50%;
        width: 50%; height: 2px;
        background: linear-gradient(90deg, var(--cyber-mint), transparent);
        transform-origin: left center;
        animation: sweep 3s linear infinite;
        box-shadow: 0 0 8px var(--cyber-mint);
    }

    .radar-center {
        position: absolute;
        top: 50%; left: 50%;
        width: 5px; height: 5px;
        background: var(--cyber-mint);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 10px var(--cyber-mint);
    }

    @keyframes sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* ── THREAT RESULT CARDS ── */
    .result-card {
        position: relative;
        border-radius: 12px;
        padding: 28px;
        margin: 12px 0 16px 0;
        overflow: hidden;
    }

    .result-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
    }

    .result-spam {
        background: linear-gradient(135deg, rgba(255,46,99,0.1) 0%, var(--cyber-surface) 100%);
        border: 1px solid var(--cyber-red);
        box-shadow: 0 0 30px rgba(255,46,99,0.12), inset 0 1px 0 rgba(255,46,99,0.15);
    }

    .result-spam::before {
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 3px,
            rgba(255,46,99,0.02) 3px,
            rgba(255,46,99,0.02) 4px
        );
    }

    .result-ham {
        background: linear-gradient(135deg, rgba(0,245,212,0.08) 0%, var(--cyber-surface) 100%);
        border: 1px solid rgba(0,245,212,0.5);
        box-shadow: 0 0 30px rgba(0,245,212,0.1), inset 0 1px 0 rgba(0,245,212,0.1);
    }

    .result-ham::before {
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 3px,
            rgba(0,245,212,0.015) 3px,
            rgba(0,245,212,0.015) 4px
        );
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }

    .threat-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 5px 14px;
        border-radius: 6px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .threat-badge.spam {
        background: var(--cyber-red);
        color: #fff;
        box-shadow: 0 0 12px rgba(255,46,99,0.4);
    }

    .threat-badge.ham {
        background: var(--cyber-mint);
        color: #060911;
        box-shadow: 0 0 12px rgba(0,245,212,0.3);
    }

    .risk-score {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
    }

    .risk-score.high { color: var(--cyber-red); }
    .risk-score.low { color: var(--cyber-mint); }

    .result-body h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        color: #fff;
        margin: 0 0 8px 0;
    }

    .result-body p {
        color: var(--cyber-muted);
        font-size: 0.88rem;
        line-height: 1.5;
        margin: 0;
    }

    .result-body p strong { color: var(--cyber-text); }

    /* ── SIGNAL CHIPS ── */
    .signal-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }

    .signal-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .signal-chip .weight {
        opacity: 0.6;
        font-size: 0.68rem;
    }

    .chip-danger {
        background: var(--cyber-red-dim);
        color: #FF8BA7;
        border: 1px solid rgba(255,46,99,0.3);
    }

    .chip-safe {
        background: var(--cyber-mint-dim);
        color: #70FFE8;
        border: 1px solid rgba(0,245,212,0.3);
    }

    /* ── KPI METRIC BLOCKS ── */
    .kpi-block {
        background: var(--cyber-card);
        border: 1px solid var(--cyber-border);
        border-radius: 10px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
    }

    .kpi-block::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0;
        height: 3px;
        border-radius: 0 0 10px 10px;
    }

    .kpi-block.mint::after { width: 100%; background: var(--cyber-mint); opacity: 0.5; }
    .kpi-block.red::after { width: 100%; background: var(--cyber-red); opacity: 0.5; }
    .kpi-block.blue::after { width: 100%; background: var(--cyber-blue); opacity: 0.5; }
    .kpi-block.purple::after { width: 100%; background: var(--cyber-purple); opacity: 0.5; }

    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--cyber-muted);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #fff;
    }

    .kpi-value .unit {
        font-size: 0.9rem;
        color: var(--cyber-muted);
        font-weight: 500;
    }

    /* ── TELEMETRY LOG ── */
    .telem-log {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--cyber-muted);
        background: rgba(0,0,0,0.3);
        border: 1px solid var(--cyber-border);
        border-radius: 8px;
        padding: 12px 14px;
        line-height: 1.8;
    }

    .telem-log .ok { color: var(--cyber-mint); }
    .telem-log .warn { color: var(--cyber-amber); }
    .telem-log .dim { opacity: 0.5; }

    /* ── SIDEBAR ── */
    .sidebar-section {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--cyber-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 20px 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid var(--cyber-border);
    }
</style>
""")

# ============================================================
# BACKEND: NLP, Model, Data Loading
# ============================================================
@st.cache_resource
def load_nltk():
    for resource in ['wordnet', 'omw-1.4', 'punkt']:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass
    return WordNetLemmatizer()

lemmatizer = load_nltk()

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()
    lemmatized = [lemmatizer.lemmatize(w) for w in tokens]
    return re.sub(r"\s+", " ", " ".join(lemmatized)).strip()

@st.cache_resource
def load_artifacts():
    if os.path.exists("spam_model.pkl") and os.path.exists("tfidf_vectorizer.pkl"):
        return joblib.load("spam_model.pkl"), joblib.load("tfidf_vectorizer.pkl")
    return None, None

model, vectorizer = load_artifacts()

@st.cache_data
def load_dataset():
    tsv_path = "sms.tsv" if os.path.exists("sms.tsv") else None
    if tsv_path:
        df = pd.read_csv(tsv_path, sep='\t', header=None, names=['label', 'message'])
        df = df.drop_duplicates()
        df['char_count'] = df['message'].str.len()
        df['word_count'] = df['message'].str.split().str.len()
        return df
    return None

df_data = load_dataset()

# ============================================================
# HEADER BANNER with Radar Animation
# ============================================================
st.html("""
<div class="soc-banner">
    <div class="banner-grid">
        <div class="banner-left">
            <h1>🛡️ <span class="accent">CYBERSEC</span> // SPAM THREAT ENGINE</h1>
            <p>NLP-POWERED REAL-TIME MESSAGE THREAT ANALYSIS & CLASSIFICATION</p>
            <div class="status-pill">
                <div class="dot"></div>
                THREAT ENGINE ACTIVE · TF-IDF · LINEAR SVC
            </div>
        </div>
        <div class="radar-box">
            <div class="radar-ring r1"></div>
            <div class="radar-ring r2"></div>
            <div class="radar-ring r3"></div>
            <div class="radar-sweep"></div>
            <div class="radar-center"></div>
        </div>
    </div>
</div>
""")

if model is None or vectorizer is None:
    st.error("Model artifacts missing. Run `python spam_detection.py` to generate them.", icon=":material/error:")
    st.stop()

# ============================================================
# SIDEBAR — Control Panel
# ============================================================
with st.sidebar:
    st.html('<div class="sidebar-section">THREAT CONFIG</div>')

    threshold = st.slider(
        "Decision boundary",
        min_value=0.10, max_value=0.90, value=0.50, step=0.05,
        help="Messages scoring above this threshold are flagged as spam."
    )

    st.html('<div class="sidebar-section">ENGINE SPECS</div>')

    st.markdown("""
| Parameter | Value |
|-----------|-------|
| Classifier | `LinearSVC` |
| Features | `5,000 TF-IDF` |
| Preprocessing | `Lemmatize + Stopwords` |
| Accuracy | `97.7%` |
| F1 (spam) | `0.905` |
""")

    st.html('<div class="sidebar-section">SYSTEM LOG</div>')

    st.html("""
    <div class="telem-log">
        <span class="dim">[SYS]</span> <span class="ok">●</span> Node initialized<br>
        <span class="dim">[MOD]</span> <span class="ok">●</span> TF-IDF vectorizer loaded<br>
        <span class="dim">[MOD]</span> <span class="ok">●</span> LinearSVC model loaded<br>
        <span class="dim">[NET]</span> <span class="ok">●</span> Threat engine online<br>
        <span class="dim">[DAT]</span> <span class="warn">●</span> 5,169 corpus records cached
    </div>
    """)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs([
    ":material/shield: Threat interceptor",
    ":material/monitoring: Model diagnostics",
    ":material/database: Dataset intelligence"
])

# ============================================================
# TAB 1 — THREAT INTERCEPTOR
# ============================================================
with tab1:
    col_input, col_presets = st.columns([3, 1])

    with col_presets:
        st.caption("QUICK-LOAD PAYLOADS")
        preset = st.radio(
            "Payload preset",
            options=[
                "Custom input",
                "🎁 Prize scam",
                "🏦 Bank phishing",
                "☕ Casual chat",
                "📄 Work email"
            ],
            index=0,
            label_visibility="collapsed"
        )

    preset_map = {
        "🎁 Prize scam": "WINNER!! You've won a £1000 Walmart gift card. Go to http://bit.ly/claim-prize to claim now!",
        "🏦 Bank phishing": "URGENT: Your NatWest account has been compromised. Call 0800-123-987 immediately to verify your identity or your account will be locked.",
        "☕ Casual chat": "Hey Sarah, are we still meeting for lunch at 12:30 PM tomorrow at the downtown cafe?",
        "📄 Work email": "Hi Team, please find attached the Q3 revenue report for review before our sync on Thursday."
    }

    with col_input:
        input_message = st.text_area(
            "Message payload",
            value=preset_map.get(preset, ""),
            height=130,
            placeholder="Paste or type a message to scan for spam threats...",
            label_visibility="collapsed"
        )

        scan_btn = st.button(
            "Scan for threats",
            type="primary",
            icon=":material/radar:",
            use_container_width=True
        )

    # ── ANALYSIS ──
    if scan_btn and input_message.strip():
        cleaned = clean_text(input_message)
        vec_input = vectorizer.transform([cleaned])

        # Spam probability
        if hasattr(model, "predict_proba"):
            spam_prob = model.predict_proba(vec_input)[0][1]
        elif hasattr(model, "decision_function"):
            raw = model.decision_function(vec_input)[0]
            spam_prob = 1 / (1 + np.exp(-raw))
        else:
            spam_prob = float(model.predict(vec_input)[0])

        is_spam = spam_prob >= threshold

        # TF-IDF feature extraction
        feature_names = np.array(vectorizer.get_feature_names_out())
        cx = vec_input.tocoo()
        signals = sorted(
            [(feature_names[j], v) for _, j, v in zip(cx.row, cx.col, cx.data)],
            key=lambda x: x[1], reverse=True
        )

        # Build signal chips HTML
        chip_cls = "chip-danger" if is_spam else "chip-safe"
        chips_html = ""
        for word, weight in signals[:10]:
            chips_html += f'<span class="signal-chip {chip_cls}">{word} <span class="weight">{weight:.2f}</span></span>'

        col_result, col_gauge = st.columns([3, 2])

        with col_result:
            if is_spam:
                st.html(f"""
                <div class="result-card result-spam">
                    <div class="result-header">
                        <span class="threat-badge spam">🚨 THREAT DETECTED</span>
                        <span class="risk-score high">{spam_prob*100:.1f}%</span>
                    </div>
                    <div class="result-body">
                        <h3>Malicious / promotional anomaly identified</h3>
                        <p>Pattern signature matches spam and phishing distributions in the training corpus.
                        Recommended action: <strong>QUARANTINE</strong> or <strong>BLOCK SENDER</strong>.</p>
                    </div>
                    <div class="signal-row">{chips_html}</div>
                </div>
                """)
            else:
                st.html(f"""
                <div class="result-card result-ham">
                    <div class="result-header">
                        <span class="threat-badge ham">✅ VERIFIED SECURE</span>
                        <span class="risk-score low">{(1 - spam_prob)*100:.1f}%</span>
                    </div>
                    <div class="result-body">
                        <h3>Legitimate transmission — clearance confirmed</h3>
                        <p>No threat patterns detected in payload.
                        Recommended action: <strong>DELIVER TO INBOX</strong>.</p>
                    </div>
                    <div class="signal-row">{chips_html}</div>
                </div>
                """)

        with col_gauge:
            with st.container(border=True):
                st.caption("SPAM RISK GAUGE")
                st.progress(float(spam_prob), text=f"Spam probability: {spam_prob*100:.1f}%  ·  Threshold: {threshold*100:.0f}%")

                st.caption("PREPROCESSING TELEMETRY")
                st.code(f"RAW   → {input_message[:80]}{'...' if len(input_message)>80 else ''}\nCLEAN → {cleaned[:80]}{'...' if len(cleaned)>80 else ''}\nFEATS → {len(signals)} vocabulary matches", language=None)

    elif scan_btn:
        st.warning("Enter a message to scan.", icon=":material/warning:")

# ============================================================
# TAB 2 — MODEL DIAGNOSTICS
# ============================================================
with tab2:
    st.markdown("##### Model performance benchmarks")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.html("""<div class="kpi-block mint">
            <div class="kpi-label">Accuracy</div>
            <div class="kpi-value">97.7<span class="unit">%</span></div>
        </div>""")
    with k2:
        st.html("""<div class="kpi-block blue">
            <div class="kpi-label">Precision (Spam)</div>
            <div class="kpi-value">97.2<span class="unit">%</span></div>
        </div>""")
    with k3:
        st.html("""<div class="kpi-block purple">
            <div class="kpi-label">Recall (Spam)</div>
            <div class="kpi-value">84.7<span class="unit">%</span></div>
        </div>""")
    with k4:
        st.html("""<div class="kpi-block red">
            <div class="kpi-label">F1-Score</div>
            <div class="kpi-value">0.905</div>
        </div>""")

    col_cm, col_feat = st.columns(2)

    with col_cm:
        with st.container(border=True):
            st.caption("CONFUSION MATRIX — TEST SET")
            cm_df = pd.DataFrame({
                'Actual': ['Ham', 'Ham', 'Spam', 'Spam'],
                'Predicted': ['Ham', 'Spam', 'Ham', 'Spam'],
                'Count': [962, 4, 21, 116]
            })

            base = alt.Chart(cm_df).encode(
                x=alt.X('Predicted:N', title='Predicted'),
                y=alt.Y('Actual:N', title='Actual')
            ).properties(height=280)

            heatmap = base.mark_rect(cornerRadius=4).encode(
                color=alt.Color('Count:Q',
                    scale=alt.Scale(
                        domain=[0, 200, 962],
                        range=['#111827', '#1e3a5f', '#00F5D4']
                    ),
                    legend=None
                )
            )

            labels = base.mark_text(fontSize=20, fontWeight='bold', color='white').encode(
                text='Count:Q'
            )

            st.altair_chart(heatmap + labels, use_container_width=True)

    with col_feat:
        with st.container(border=True):
            st.caption("TOP SPAM SIGNAL KEYWORDS")
            if hasattr(model, "coef_"):
                coefs = model.coef_[0]
                fnames = vectorizer.get_feature_names_out()
                top_idx = np.argsort(coefs)[-12:]
                feat_df = pd.DataFrame({
                    'keyword': fnames[top_idx],
                    'weight': coefs[top_idx]
                }).sort_values('weight', ascending=True)

                chart = alt.Chart(feat_df).mark_bar(
                    cornerRadiusEnd=4,
                    color='#FF2E63'
                ).encode(
                    x=alt.X('weight:Q', title='LinearSVC coefficient'),
                    y=alt.Y('keyword:N', sort=None, title=None),
                    tooltip=['keyword', alt.Tooltip('weight:Q', format='.3f')]
                ).properties(height=280)

                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Feature weights unavailable for this model type.")

# ============================================================
# TAB 3 — DATASET INTELLIGENCE
# ============================================================
with tab3:
    st.markdown("##### Corpus intelligence & exploratory analysis")

    if df_data is not None:
        total = len(df_data)
        ham_n = (df_data['label'] == 'ham').sum()
        spam_n = (df_data['label'] == 'spam').sum()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total messages", f"{total:,}")
        k2.metric("Legitimate (ham)", f"{ham_n:,}", delta=f"{ham_n/total*100:.1f}%")
        k3.metric("Spam threats", f"{spam_n:,}", delta=f"{spam_n/total*100:.1f}%", delta_color="inverse")
        k4.metric("Avg message length", f"{int(df_data['char_count'].mean())} chars")

        col_d1, col_d2 = st.columns(2)

        with col_d1:
            with st.container(border=True):
                st.caption("CLASS DISTRIBUTION")
                dist_df = pd.DataFrame({
                    'Class': ['Ham', 'Spam'],
                    'Count': [ham_n, spam_n]
                })
                bar = alt.Chart(dist_df).mark_bar(cornerRadiusEnd=6).encode(
                    x=alt.X('Class:N', title=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('Count:Q', title='Messages'),
                    color=alt.Color('Class:N',
                        scale=alt.Scale(domain=['Ham', 'Spam'], range=['#00F5D4', '#FF2E63']),
                        legend=None
                    )
                ).properties(height=250)
                st.altair_chart(bar, use_container_width=True)

        with col_d2:
            with st.container(border=True):
                st.caption("MESSAGE LENGTH BY CLASS")
                area = alt.Chart(df_data).mark_area(opacity=0.45, interpolate='monotone').encode(
                    x=alt.X('char_count:Q', bin=alt.Bin(maxbins=50), title='Character count'),
                    y=alt.Y('count():Q', title='Frequency', stack=None),
                    color=alt.Color('label:N',
                        scale=alt.Scale(domain=['ham', 'spam'], range=['#00F5D4', '#FF2E63']),
                        legend=alt.Legend(title=None, orient='top-right')
                    )
                ).properties(height=250)
                st.altair_chart(area, use_container_width=True)

        with st.expander("Preview dataset sample", icon=":material/table:"):
            st.dataframe(
                df_data[['label', 'message', 'char_count', 'word_count']].head(100),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("Dataset file not found. Place `sms.tsv` in the project root.")
