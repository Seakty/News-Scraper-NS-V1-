import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsLens · AI Article Analyzer",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS (for Streamlit shell) ─────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --ink:      #0d0d0d;
    --paper:    #f5f0e8;
    --cream:    #ede8dc;
    --accent:   #c8410a;
    --muted:    #7a7468;
    --card-bg:  #faf7f2;
    --border:   #d6cfbf;
    --radius:   4px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper) !important;
    color: var(--ink) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 780px !important;
}

.masthead {
    border-top: 4px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    padding: 1.6rem 0 1.2rem;
    margin-bottom: 0.5rem;
    text-align: center;
}
.masthead-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 900;
    line-height: 1;
    color: var(--ink);
    margin: 0;
    letter-spacing: -0.02em;
}
.masthead-title span { color: #c8410a; }
.masthead-sub {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 0.7rem;
    font-weight: 300;
    letter-spacing: 0.04em;
}
.masthead-rule {
    width: 40px; height: 2px;
    background: #c8410a;
    margin: 0.9rem auto 0;
}

.dateline {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-align: right;
    padding: 0.4rem 0 0.8rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}

.input-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.8rem 0.5rem;
    margin-bottom: 1.6rem;
    box-shadow: 2px 3px 0 var(--border);
}
.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
    display: block;
}

.stTextInput > div > div > input {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--ink) !important;
    padding: 0.65rem 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c8410a !important;
    box-shadow: 0 0 0 2px rgba(200,65,10,0.1) !important;
}

.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    margin-top: 0.4rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #c8410a !important; }

.page-footer {
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    padding-top: 1rem;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
}
</style>
"""

# ── CSS injected inside components.html (isolated iframe) ────────────────────
COMPONENT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.article-image-container {
    width: 100%;
    height: 280px;
    overflow: hidden;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    border: 1px solid #d6cfbf;
    background-color: #ede8dc; /* placeholder color while loading */
}
.article-image {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Ensures the image fills the box without stretching */
    display: block;
}

body {
    background: transparent;
    font-family: 'DM Sans', sans-serif;
    color: #0d0d0d;
}

.result-card {
    background: #faf7f2;
    border: 1px solid #d6cfbf;
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    box-shadow: 2px 3px 0 #d6cfbf;
    animation: fadeSlide 0.4s ease forwards;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-kicker {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8410a;
    margin-bottom: 0.5rem;
}
.result-headline {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.2rem, 3vw, 1.75rem);
    font-weight: 700;
    line-height: 1.3;
    color: #0d0d0d;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #d6cfbf;
}

.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1.4rem;
}
.stat-box {
    flex: 1;
    background: white;
    border: 1px solid #d6cfbf;
    border-radius: 4px;
    padding: 0.9rem;
    text-align: center;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7a7468;
    margin-bottom: 0.35rem;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0d0d0d;
    line-height: 1.2;
}
.stat-value.positive { color: #1a6b3c; }
.stat-value.negative { color: #991f1f; }
.stat-value.neutral  { color: #4a5568; }
.stat-sub {
    font-size: 0.8rem;
    color: #7a7468;
    font-family: 'DM Sans', sans-serif;
}

.score-bar-wrap { margin-bottom: 1.6rem; }
.score-bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7a7468;
    margin-bottom: 0.4rem;
}
.score-bar-track {
    height: 6px;
    background: #ede8dc;
    border-radius: 3px;
    border: 1px solid #d6cfbf;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 3px;
}

.section-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a7468;
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #d6cfbf;
}
.summary-text {
    font-size: 0.96rem;
    line-height: 1.78;
    color: #2d2926;
    font-weight: 300;
}

.keywords-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
}
.keyword-tag {
    background: white;
    border: 1px solid #d6cfbf;
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 0.22rem 0.6rem;
    color: #0d0d0d;
    letter-spacing: 0.04em;
}
</style>
"""

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-eyebrow">Powered by AI · Agentic Analysis</div>
    <h1 class="masthead-title">News<span>Lens</span></h1>
    <p class="masthead-sub">Paste any article URL — get instant sentiment, summary &amp; insights</p>
    <div class="masthead-rule"></div>
</div>
""", unsafe_allow_html=True)

today = datetime.now().strftime("%A, %B %d, %Y").upper()
st.markdown(f'<div class="dateline">Edition · {today}</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<span class="input-label">Article URL</span>', unsafe_allow_html=True)
url = st.text_input(
    label="url_input",
    placeholder="https://www.bbc.com/news/...",
    label_visibility="collapsed",
)
analyze = st.button("🔍  Analyze Article")
st.markdown('</div>', unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze:
    if not url.strip():
        st.warning("Please enter a URL to get started.")
    else:
        with st.spinner("Agent is visiting the page and reading the article…"):
            try:
                response = requests.post(
                    "http://localhost:8000/api/process",
                    json={"url": url},
                    timeout=60,
                )
                data = response.json()
            except Exception as e:
                st.error(f"**Connection Error** — Is the backend running?\n\n`{e}`")
                st.stop()

        if "error" in data:
            st.error(f"**Backend Error:** {data['error']}")
            st.stop()

        # Extract fields
        title     = data.get("title", "Untitled Article")
        sentiment = data.get("sentiment", "N/A")
        score     = int(data.get("sentiment_score", 0))
        keywords  = data.get("keywords", [])
        summary   = data.get("summary", "No summary available.")
        main_image = data.get("main_image")

        # Sentiment label + class
        s_lower = sentiment.lower()
        if "positive" in s_lower:
            s_class, s_label = "positive", "↑ Positive"
        elif "negative" in s_lower:
            s_class, s_label = "negative", "↓ Negative"
        else:
            s_class, s_label = "neutral", "→ Neutral"

        # Score bar colour
        bar_color = "#1a6b3c" if score >= 65 else "#c9973a" if score >= 40 else "#991f1f"

        # Keyword tags
        kw_tags = "".join(f'<span class="keyword-tag">{kw}</span>' for kw in keywords)

        # Create the image HTML conditionally
        image_html = ""
        image_height_buffer = 0
        if main_image:
            # We use an onerror attribute just in case the image link is broken
            image_html = f'''
            <div class="article-image-container">
                <a href="{main_image}" target="_blank" title="Click to view full size">
                    <img src="{main_image}" alt="Article Featured Image" class="article-image" style="cursor: zoom-in;" onerror="this.parentElement.parentElement.style.display='none';">
                </a>
            </div>
            '''
            image_height_buffer = 300  # Add extra height to the iframe if image exists

        # Estimate height: base + summary lines + keyword rows
        summary_lines = max(3, len(summary) // 80)
        kw_rows = max(1, len(keywords) // 4)
        estimated_height = 420 + (summary_lines * 28) + (kw_rows * 36)

        

        result_html = f"""
        {COMPONENT_CSS}

        <div class="result-card">
            <div class="result-kicker">Analysis Complete</div>
            <div class="result-headline">{title}</div>

            {image_html} <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-label">Sentiment</div>
                    <div class="stat-value {s_class}">{s_label}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Score</div>
                    <div class="stat-value">{score}<span class="stat-sub"> / 100</span></div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Keywords</div>
                    <div class="stat-value">{len(keywords)}</div>
                </div>
            </div>

            <div class="score-bar-wrap">
                <div class="score-bar-label">
                    <span>Sentiment Intensity</span>
                    <span>{score}%</span>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width:{score}%; background:{bar_color};"></div>
                </div>
            </div>

            <div class="section-title">Summary</div>
            <p class="summary-text">{summary}</p>
        </div>

        <div class="result-card">
            <div class="section-title">Keywords &middot; {len(keywords)} found</div>
            <div class="keywords-wrap">{kw_tags}</div>
        </div>
        """
        # 2. Add the image buffer to the final height!
        final_height = estimated_height + image_height_buffer

        # 3. Render the component with the new taller height
        components.html(result_html, height=final_height, scrolling=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    NewsLens · AI-Powered Article Analysis · All rights reserved
</div>
""", unsafe_allow_html=True)

