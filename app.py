import streamlit as st
from src.ui.theme import load_theme, hero, stats_bar, resilience_sidebar, footer
from src.ui.scan_page import show_scan_page
from src.ui.profile_page import show_profile_page
from src.config.settings import fallback_status

st.set_page_config(
    page_title="GlucoGuard+ — Apne khaane ka guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom theme on every render
load_theme()

# Initialize session state
defaults = {
    "page": "scan",
    "profile": {"conditions": ["none"], "allergies": ["none"], "language": "roman_urdu", "voice_enabled": False},
    "error": None,
    "label_data": None,
    "verdict": None,
    "alternative": None,
    "audio_bytes": None,
    "speech_text": None,
    "scanned_image": None,
    "scanned_image_mime": None,
    "show_teach_mode": False,
    "demo_mode": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# === SIDEBAR ===
with st.sidebar:
    st.markdown("### 🛡️ GlucoGuard<span style='color:#F59E0B'>+</span>", unsafe_allow_html=True)
    st.caption("Pakistan's food guardian")

    st.divider()

    # Profile summary card
    st.markdown("##### 🩺 Your Profile")
    profile = st.session_state.profile
    if profile.get("conditions") and profile["conditions"] != ["none"]:
        for c in profile["conditions"]:
            st.markdown(f'<span class="gg-profile-tag">{c}</span>', unsafe_allow_html=True)
    else:
        st.caption("_No conditions set_")

    if profile.get("allergies") and profile["allergies"] != ["none"]:
        for a in profile["allergies"]:
            st.markdown(f'<span class="gg-profile-tag">⚠️ {a}</span>', unsafe_allow_html=True)

    if profile.get("voice_enabled"):
        st.markdown("🔊 **Voice: ON**")
    else:
        st.caption("🔇 Voice: OFF")

    st.divider()

    # Navigation
    if st.button("🍽️ Scan Khaana", use_container_width=True, type="primary" if st.session_state.page != "scan" else "secondary"):
        st.session_state.page = "scan"
        st.rerun()
    if st.button("🩺 Edit Profile", use_container_width=True, type="primary" if st.session_state.page != "profile" else "secondary"):
        st.session_state.page = "profile"
        st.rerun()

    st.divider()

    # Resilience layer
    fb = fallback_status()
    resilience_sidebar(fb)

    st.divider()
    st.caption("⚡ 4 OpenAI models in pipeline:")
    st.caption("👁️ gpt-4o-mini · 🧠 gpt-4o-mini")
    st.caption("🔍 gpt-4o-search · 🔊 gpt-4o-mini-tts")

# === MAIN CONTENT ===
# Use a centered column layout for readability
main_col = st.container()
with main_col:
    if st.session_state.page == "profile":
        show_profile_page()
    else:
        show_scan_page()

# Footer always at the bottom
footer()
