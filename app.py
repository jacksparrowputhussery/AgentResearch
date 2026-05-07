

import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentResearch · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (light theme) ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
    color: #1a1410;
}

.stApp {
    background: #faf8f4;
    background-image:
        radial-gradient(ellipse 70% 40% at 10% 0%, rgba(210,165,90,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(180,130,70,0.07) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8a96e' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1240px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #b8892a;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
}
.hero-eyebrow::before,
.hero-eyebrow::after {
    content: '';
    display: inline-block;
    width: 40px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c8a96e);
}
.hero-eyebrow::after {
    background: linear-gradient(90deg, #c8a96e, transparent);
}
.hero h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(3rem, 6vw, 5.2rem);
    font-weight: 900;
    line-height: 1.0;
    letter-spacing: -0.02em;
    color: #1a1410;
    margin: 0 0 0.8rem;
}
.hero h1 em {
    font-style: italic;
    color: #b8892a;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    font-style: italic;
    color: #7a6a55;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.75;
}
.hero-rule {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin: 2rem auto;
    max-width: 400px;
}
.hero-rule-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #d4b870, transparent);
}
.hero-rule-diamond {
    width: 8px; height: 8px;
    background: #c8a96e;
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* ── Input card ── */
.input-card {
    background: #ffffff;
    border: 1px solid #e8dcc8;
    border-radius: 14px;
    padding: 2rem 2.5rem 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.04),
        0 4px 16px rgba(180,140,60,0.06),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

/* ── Input overrides ── */
.stTextInput > div > div > input {
    background: #faf8f4 !important;
    border: 1.5px solid #d8c8a8 !important;
    border-radius: 9px !important;
    color: #1a1410 !important;
    font-family: 'Source Serif 4', Georgia, serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #b8892a !important;
    box-shadow: 0 0 0 3px rgba(184,137,42,0.10) !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input::placeholder {
    color: #b0a090 !important;
    font-style: italic !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #b8892a !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #c8a232 0%, #a07020 100%) !important;
    color: #fff9ee !important;
    font-family: 'Playfair Display', Georgia, serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.72rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow:
        0 2px 8px rgba(180,130,30,0.25),
        0 1px 0 rgba(255,255,255,0.15) inset !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(180,130,30,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline cards ── */
.step-card {
    background: #ffffff;
    border: 1px solid #e8dcc8;
    border-radius: 12px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.step-card.active {
    border-color: #c8a232;
    background: #fffdf5;
    box-shadow: 0 2px 12px rgba(200,162,50,0.12);
}
.step-card.done {
    border-color: #7ab87a;
    background: #f6faf5;
    box-shadow: 0 1px 6px rgba(100,180,100,0.10);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
    background: #e8dcc8;
    transition: background 0.3s;
}
.step-card.active::before { background: #c8a232; }
.step-card.done::before   { background: #5aa85a; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: #c8a232;
    opacity: 0.8;
}
.step-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #1a1410;
}
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #c0b098; }
.status-running  { color: #c8a232; }
.status-done     { color: #5aa85a; }
.step-desc {
    font-size: 0.8rem;
    color: #9a8878;
    margin-top: 0.3rem;
    font-style: italic;
    padding-left: 2.5rem;
}

/* ── Result panels ── */
.result-panel {
    background: #ffffff;
    border: 1px solid #e8dcc8;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b8892a;
    margin-bottom: 0.9rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #ede0c8;
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.85;
    color: #3a2e22;
    white-space: pre-wrap;
    font-family: 'Source Serif 4', Georgia, serif;
}

/* ── Report & feedback ── */
.report-panel {
    background: #ffffff;
    border: 1.5px solid #d4b870;
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
    margin-top: 1rem;
    box-shadow:
        0 2px 12px rgba(200,160,60,0.08),
        0 1px 0 rgba(255,255,255,0.9) inset;
}
.feedback-panel {
    background: #ffffff;
    border: 1.5px solid #8ac88a;
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
    margin-top: 1rem;
    box-shadow:
        0 2px 12px rgba(100,180,100,0.07),
        0 1px 0 rgba(255,255,255,0.9) inset;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
}
.panel-label.gold {
    color: #b8892a;
    border-bottom: 1px solid #e8d498;
}
.panel-label.green {
    color: #4a8a4a;
    border-bottom: 1px solid #b8d8b8;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #faf6ee !important;
    color: #b8892a !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    border: 1.5px solid #d4b870 !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.15s, box-shadow 0.15s !important;
    box-shadow: none !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: #f5ede0 !important;
    box-shadow: 0 2px 8px rgba(200,160,50,0.15) !important;
}

/* ── Spinner ── */
.stSpinner > div { color: #b8892a !important; }

/* ── Expander ── */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #9a8878 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #1a1410;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #d4b870, transparent);
}

/* ── Tag chips ── */
.chip {
    display: inline-block;
    background: #f5f0e8;
    border: 1px solid #ddd0b8;
    border-radius: 20px;
    padding: 0.22rem 0.75rem;
    font-size: 0.74rem;
    color: #7a6a50;
    font-family: 'Source Serif 4', Georgia, serif;
    font-style: italic;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}

/* ── Warning ── */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid #e8d498 !important;
    background: #fffbe8 !important;
}

/* ── Footer ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: #c0b098;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.1em;
    padding-top: 1.5rem;
    border-top: 1px solid #ede0c8;
}

/* ── Progress bar custom ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #c8a232, #b8892a) !important;
    border-radius: 4px !important;
}
.stProgress > div > div {
    background: #ede0c8 !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING",    "status-waiting"),
        "running": ("● RUNNING",  "status-running"),
        "done":    ("✓ DONE",     "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Agent<em>Research</em></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping,
        writing, and critiquing — to deliver a polished research report
        on any topic you choose.
    </p>
    <div class="hero-rule">
        <div class="hero-rule-line"></div>
        <div class="hero-rule-diamond"></div>
        <div class="hero-rule-line"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                     color:#b0a090;letter-spacing:0.15em;margin-right:0.5rem;">TRY →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

    # Info box
    st.markdown("""
    <div style="background:#fdf8f0;border:1px solid #e8d8b8;border-radius:10px;
                padding:1rem 1.3rem;margin-top:0.5rem;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.64rem;
                    color:#c8a232;letter-spacing:0.15em;text-transform:uppercase;
                    margin-bottom:0.5rem;">How it works</div>
        <div style="font-size:0.82rem;color:#7a6a55;line-height:1.7;font-style:italic;">
            The pipeline runs four agents in sequence: a Search Agent gathers
            current web intelligence, a Reader Agent scrapes top sources for depth,
            a Writer Chain composes a structured report, and a Critic Chain scores
            and refines the final output.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")

    # Progress indicator
    if st.session_state.running or st.session_state.done:
        steps_done = len(st.session_state.results)
        progress_val = steps_done / 4
        st.markdown(f"""
        <div style="margin-top:1rem;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.64rem;
                        color:#b8892a;letter-spacing:0.12em;margin-bottom:0.4rem;">
                PROGRESS · {steps_done}/4 STEPS
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_val)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic to begin.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search Agent is gathering information…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer is composing the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic is reviewing and scoring the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,#d4b870,transparent);
                margin:2rem 0 0.5rem;"></div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label gold">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">Critic Feedback & Score</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    AgentResearch &nbsp;·&nbsp; Powered by LangChain multi-agent pipeline &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)