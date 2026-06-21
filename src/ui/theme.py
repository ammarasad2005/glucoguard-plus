"""Custom CSS theme for GlucoGuard+. Loaded once on app startup."""
import streamlit as st

def load_theme():
    """Inject custom CSS into the Streamlit app."""
    st.markdown("""
    <style>
    /* === ROOT THEME === */
    :root {
        --gg-primary: #0F766E;          /* Teal-700 — trust + health */
        --gg-primary-dark: #115E59;     /* Teal-800 */
        --gg-primary-light: #CCFBF1;    /* Teal-100 */
        --gg-accent: #F59E0B;           /* Amber-500 — the "+" */
        --gg-danger: #DC2626;           /* Red-600 */
        --gg-warning: #D97706;          /* Amber-600 */
        --gg-success: #059669;          /* Emerald-600 */
        --gg-bg: #F8FAFC;               /* Slate-50 */
        --gg-card: #FFFFFF;
        --gg-border: #E2E8F0;           /* Slate-200 */
        --gg-text: #0F172A;             /* Slate-900 */
        --gg-text-muted: #64748B;       /* Slate-500 */
    }

    /* === GLOBAL === */
    .stApp {
        background: linear-gradient(180deg, #F0FDFA 0%, #F8FAFC 280px);
    }
    .stApp > header {
        background: transparent;
    }

    /* === HERO HEADER === */
    .gg-hero {
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(15, 118, 110, 0.15);
        position: relative;
        overflow: hidden;
    }
    .gg-hero::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.25) 0%, transparent 70%);
        border-radius: 50%;
    }
    .gg-hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
        position: relative;
    }
    .gg-hero p {
        font-size: 1.05rem;
        margin: 0;
        opacity: 0.92;
        position: relative;
    }
    .gg-hero .gg-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.75rem;
        border: 1px solid rgba(245, 158, 11, 0.4);
        position: relative;
    }

    /* === STATS BAR (under hero) === */
    .gg-stats {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .gg-stat {
        flex: 1;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--gg-border);
        text-align: center;
    }
    .gg-stat .gg-stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--gg-primary);
        line-height: 1;
    }
    .gg-stat .gg-stat-label {
        font-size: 0.75rem;
        color: var(--gg-text-muted);
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* === VERDICT CARD (the hero result) === */
    .gg-verdict {
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border-left: 6px solid;
        position: relative;
        overflow: hidden;
    }
    .gg-verdict.gg-safe {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left-color: var(--gg-success);
    }
    .gg-verdict.gg-moderate {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left-color: var(--gg-warning);
    }
    .gg-verdict.gg-avoid {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left-color: var(--gg-danger);
    }
    .gg-verdict-label {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }
    .gg-verdict.gg-safe .gg-verdict-label {
        background: var(--gg-success);
        color: white;
    }
    .gg-verdict.gg-moderate .gg-verdict-label {
        background: var(--gg-warning);
        color: white;
    }
    .gg-verdict.gg-avoid .gg-verdict-label {
        background: var(--gg-danger);
        color: white;
    }
    .gg-verdict-title {
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: var(--gg-text);
    }
    .gg-verdict-reason {
        font-size: 1.05rem;
        line-height: 1.6;
        color: var(--gg-text);
        margin: 0;
    }

    /* === SECTION CARDS === */
    .gg-section {
        background: white;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--gg-border);
    }
    .gg-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        color: var(--gg-text);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* === HIDDEN SUGAR PILLS === */
    .gg-sugar-pill {
        display: inline-block;
        background: #FEE2E2;
        color: #991B1B;
        padding: 0.4rem 0.85rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
        border: 1px solid #FCA5A5;
    }
    .gg-sugar-gi {
        font-size: 0.7rem;
        color: #7F1D1D;
        margin-left: 0.25rem;
        opacity: 0.8;
    }

    /* === ALLERGEN BADGES === */
    .gg-allergen-badge {
        display: inline-block;
        background: #FEE2E2;
        color: var(--gg-danger);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        margin: 0.25rem;
        border: 2px solid var(--gg-danger);
    }

    /* === ALTERNATIVE CARD === */
    .gg-alternative {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 1px solid #BAE6FD;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .gg-alternative-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0C4A6E;
        margin: 0 0 0.5rem 0;
    }
    .gg-alternative-brand {
        font-size: 0.9rem;
        color: #075985;
        margin-bottom: 0.75rem;
    }
    .gg-buy-btn {
        display: inline-block;
        background: var(--gg-primary);
        color: white !important;
        padding: 0.6rem 1.25rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 0.5rem;
        transition: background 0.2s;
    }
    .gg-buy-btn:hover {
        background: var(--gg-primary-dark);
    }

    /* === VOICE PLAYER === */
    .gg-voice {
        background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%);
        border: 1px solid #E9D5FF;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .gg-voice-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #6B21A8;
        margin: 0 0 0.25rem 0;
    }
    .gg-voice-caption {
        font-size: 0.85rem;
        color: #7E22CE;
        margin-bottom: 1rem;
    }

    /* === STEP INDICATOR (progress) === */
    .gg-steps {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    .gg-step {
        flex: 1;
        min-width: 120px;
        background: white;
        padding: 0.75rem;
        border-radius: 10px;
        border: 1px solid var(--gg-border);
        text-align: center;
        font-size: 0.85rem;
    }
    .gg-step-icon {
        font-size: 1.5rem;
        display: block;
        margin-bottom: 0.25rem;
    }
    .gg-step-label {
        color: var(--gg-text-muted);
        font-weight: 500;
    }

    /* === SIDEBAR POLISH === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0FDFA 100%);
        border-right: 1px solid var(--gg-border);
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: white;
        border: 1px solid var(--gg-border);
        color: var(--gg-text);
        font-weight: 600;
        transition: all 0.2s;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: var(--gg-primary);
        color: white;
        border-color: var(--gg-primary);
    }

    /* === PRIMARY BUTTON === */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--gg-primary) 0%, var(--gg-primary-dark) 100%);
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.65rem 1.5rem;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
        transition: all 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(15, 118, 110, 0.35);
    }

    /* === FILE UPLOADER === */
    .stFileUploader {
        border: 2px dashed var(--gg-border);
        border-radius: 12px;
        padding: 1rem;
        transition: border-color 0.2s;
    }
    .stFileUploader:hover {
        border-color: var(--gg-primary);
    }

    /* === METRICS === */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--gg-border);
    }
    [data-testid="stMetric"] label {
        color: var(--gg-text-muted);
        font-size: 0.8rem;
        font-weight: 500;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--gg-text);
    }

    /* === EXPANDERS === */
    .stExpander {
        border: 1px solid var(--gg-border);
        border-radius: 10px;
        background: white;
        margin-bottom: 0.5rem;
    }

    /* === RESILIENCE LAYER === */
    .gg-resilience {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    .gg-resilience-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0;
        font-size: 0.85rem;
    }

    /* === FOOTER === */
    .gg-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: var(--gg-text-muted);
        font-size: 0.85rem;
        border-top: 1px solid var(--gg-border);
        margin-top: 2rem;
    }
    .gg-footer a {
        color: var(--gg-primary);
        text-decoration: none;
    }

    /* === ANIMATIONS === */
    @keyframes gg-fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .gg-fade-in {
        animation: gg-fade-in 0.4s ease-out;
    }

    /* === PROFILE PAGE BADGES === */
    .gg-profile-tag {
        display: inline-block;
        background: var(--gg-primary-light);
        color: var(--gg-primary-dark);
        padding: 0.4rem 0.85rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def hero():
    """Render the hero header."""
    st.markdown("""
    <div class="gg-hero gg-fade-in">
        <h1>🛡️ GlucoGuard<span style="color: #FCD34D;">+</span></h1>
        <p>Apne khaane ka guard banayein. Awaaz mein. Roman Urdu mein.</p>
        <span class="gg-badge">⚡ 4 AI models · Pakistan ke 33M diabetes patients ke liye</span>
    </div>
    """, unsafe_allow_html=True)


def stats_bar():
    """Render the impact stats bar."""
    st.markdown("""
    <div class="gg-stats gg-fade-in">
        <div class="gg-stat">
            <div class="gg-stat-value">33M</div>
            <div class="gg-stat-label">Pakistanis<br>with diabetes</div>
        </div>
        <div class="gg-stat">
            <div class="gg-stat-value">40%</div>
            <div class="gg-stat-label">Adults who<br>can't read</div>
        </div>
        <div class="gg-stat">
            <div class="gg-stat-value">50+</div>
            <div class="gg-stat-label">Hidden sugar<br>names detected</div>
        </div>
        <div class="gg-stat">
            <div class="gg-stat-value">4</div>
            <div class="gg-stat-label">AI models<br>in one scan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def verdict_card(verdict: dict):
    """Render the polished verdict card."""
    v = verdict.get("verdict", "UNKNOWN")
    color = verdict.get("verdict_color", "green")
    reason = verdict.get("verdict_reason_roman_urdu", "")

    css_class = {"green": "gg-safe", "yellow": "gg-moderate", "red": "gg-avoid"}.get(color, "gg-safe")
    icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(color, "🟢")
    label_text = {"green": "SAFE — Aap kha sakte hain", "yellow": "MODERATE — Thoda kha lein", "red": "AVOID — Munasib nahi"}.get(color, v)

    st.markdown(f"""
    <div class="gg-verdict {css_class} gg-fade-in">
        <span class="gg-verdict-label">{icon} {v}</span>
        <h2 class="gg-verdict-title">{label_text}</h2>
        <p class="gg-verdict-reason">{reason}</p>
    </div>
    """, unsafe_allow_html=True)


def section_card(title: str, icon: str = ""):
    """Open a styled section card. Use as context manager."""
    st.markdown(f"""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)
    # Note: this just renders the header. Caller can use st.container() for content.


def hidden_sugar_pills(sugars: list):
    """Render hidden sugars as inline pills."""
    if not sugars:
        st.markdown('<div class="gg-section"><h3 class="gg-section-title">❗ Chhupi hui cheeniyan</h3><p style="color: var(--gg-success); font-weight: 600;">✅ Koi chhupi hui cheeni nahi mili</p></div>', unsafe_allow_html=True)
        return

    pills_html = ""
    for s in sugars:
        name = s.get("name", "Unknown")
        gi = s.get("glycemic_index")
        gi_html = f'<span class="gg-sugar-gi">GI {gi}</span>' if gi else ""
        pills_html += f'<span class="gg-sugar-pill">{name}{gi_html}</span>'

    concerns_html = ""
    for s in sugars[:3]:
        concern = s.get("concern_roman_urdu", "")
        if concern:
            concerns_html += f'<p style="font-size: 0.9rem; color: var(--gg-text-muted); margin: 0.5rem 0 0.5rem 0.5rem;">• <strong>{s.get("name", "")}</strong>: {concern}</p>'

    st.markdown(f"""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">❗ Chhupi hui cheeniyan ({len(sugars)})</h3>
        <div>{pills_html}</div>
        {concerns_html}
    </div>
    """, unsafe_allow_html=True)


def allergen_badges(allergens: list):
    """Render allergens as red badges."""
    if not allergens:
        st.markdown('<div class="gg-section"><h3 class="gg-section-title">⚠️ Allergy Alert</h3><p style="color: var(--gg-success); font-weight: 600;">✅ Aap ki allergy ka koi ingredient nahi mila</p></div>', unsafe_allow_html=True)
        return

    badges_html = ""
    for a in allergens:
        cat = a.get("allergen", "").upper()
        badges_html += f'<span class="gg-allergen-badge">🚨 {cat}</span>'

    notes_html = ""
    for a in allergens:
        matching = a.get("matching_ingredient", "")
        note = a.get("note_roman_urdu", "")
        notes_html += f'<p style="margin: 0.5rem 0 0.5rem 0.5rem; font-size: 0.9rem;"><strong>{a.get("allergen", "").upper()}</strong> ({matching}): {note}</p>'

    st.markdown(f"""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">⚠️ Allergy Alert ({len(allergens)})</h3>
        <div>{badges_html}</div>
        {notes_html}
    </div>
    """, unsafe_allow_html=True)


def alternative_card(alt: dict):
    """Render the live web search alternative card."""
    product = alt.get("alternative_product", "")
    brand = alt.get("alternative_brand", "")
    why = alt.get("why_better_roman_urdu", "")
    price = alt.get("estimated_price_pkr")
    stores = alt.get("where_to_buy", [])
    link = alt.get("online_link")

    price_html = f'<div style="font-size: 1.5rem; font-weight: 800; color: var(--gg-primary); margin: 0.5rem 0;">Rs. {price}</div>' if price else '<div style="color: var(--gg-text-muted); margin: 0.5rem 0;">Keemat: N/A</div>'
    stores_html = f'<div style="font-size: 0.9rem; color: #075985; margin-bottom: 0.75rem;">📍 {", ".join(stores)}</div>' if stores else ""
    link_html = f'<a href="{link}" target="_blank" class="gg-buy-btn">🛒 Online Order</a>' if link else ""

    st.markdown(f"""
    <div class="gg-alternative gg-fade-in">
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--gg-accent); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">🔍 Live Web Search Result</div>
        <h3 class="gg-alternative-title">{product}</h3>
        <div class="gg-alternative-brand">by {brand or "N/A"}</div>
        {price_html}
        {stores_html}
        <p style="margin: 0.75rem 0; line-height: 1.6;">{why}</p>
        {link_html}
    </div>
    """, unsafe_allow_html=True)


def voice_card():
    """Wrap the audio player in a styled card. Use st.audio() inside a container after calling this."""
    st.markdown("""
    <div class="gg-voice gg-fade-in">
        <h3 class="gg-voice-title">🔊 Suniye — Verdict Awaaz Mein</h3>
        <p class="gg-voice-caption">Yeh GlucoGuard+ ka '+' feature hai — 40% anpadh logon ke liye.</p>
    </div>
    """, unsafe_allow_html=True)


def step_indicator(current_step: int = 0):
    """Show the 4-step pipeline indicator. current_step = 0..4 (4 = done)."""
    steps = [
        ("👁️", "Label Scan", "gpt-4o-mini"),
        ("🧠", "Verdict", "gpt-4o-mini"),
        ("🔍", "Alternative", "gpt-4o-search"),
        ("🔊", "Voice", "gpt-4o-mini-tts"),
    ]
    items = ""
    for i, (icon, label, model) in enumerate(steps):
        status = "✅" if i < current_step else ("⏳" if i == current_step else "○")
        items += f"""
        <div class="gg-step">
            <span class="gg-step-icon">{icon}</span>
            <div class="gg-step-label">{label}</div>
            <div style="font-size: 0.7rem; color: var(--gg-text-muted); margin-top: 0.2rem;">{status} {model}</div>
        </div>
        """

    st.markdown(f'<div class="gg-steps gg-fade-in">{items}</div>', unsafe_allow_html=True)


def resilience_sidebar(fb: dict):
    """Render the resilience layer in the sidebar."""
    items = ""
    labels = {"gemini": "Gemini (vision)", "groq": "Groq (reasoning)", "tavily": "Tavily (search)", "google_cse": "Google Search (CSE)", "glm": "GLM (Zhipu AI)", "edge_tts": "edge-tts (voice)"}
    for k, v in fb.items():
        icon = "✅" if v else "⚠️"
        items += f'<div class="gg-resilience-item">{icon} {labels.get(k, k)}</div>'

    st.markdown(f"""
    <div class="gg-resilience">
        <div style="font-weight: 700; font-size: 0.9rem; color: var(--gg-primary-dark); margin-bottom: 0.5rem;">🛡️ Resilience Layer</div>
        <div style="font-size: 0.75rem; color: var(--gg-text-muted); margin-bottom: 0.5rem;">OpenAI primary · auto-fallback</div>
        {items}
    </div>
    """, unsafe_allow_html=True)


def footer():
    """Render the app footer."""
    st.markdown("""
    <div class="gg-footer">
        <p>🛡️ <strong>GlucoGuard+</strong> · National AI Hackathon · FAST NUCES Islamabad · 16-17 June 2026</p>
        <p>Track 5: Open Innovation · 4 OpenAI models · Multi-provider resilience</p>
    </div>
    """, unsafe_allow_html=True)
