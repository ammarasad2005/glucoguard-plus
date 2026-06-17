import streamlit as st
from src.ui.components import show_header
from src.ui.scan_page import show_scan_page
from src.ui.profile_page import show_profile_page

st.set_page_config(
    page_title="GlucoGuard+",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

defaults = {
    "page": "scan",
    "profile": {"conditions": ["none"], "allergies": ["none"], "language": "roman_urdu", "voice_enabled": False},
    "error": None,
    "label_data": None,
    "verdict": None,
    "alternative": None,
    "audio_bytes": None,
    "scanned_image": None,
    "scanned_image_mime": None,
    "show_teach_mode": False,
    "demo_mode": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.header("🛡️ GlucoGuard+")
    st.divider()
    st.header("🩺 Apni Sehat Ka Profile")
    profile = st.session_state.profile
    if profile.get("conditions") and profile["conditions"] != ["none"]:
        st.write(f"**Conditions:** {', '.join(profile['conditions'])}")
    else:
        st.write("Koi condition select nahi ki.")
    if profile.get("allergies") and profile["allergies"] != ["none"]:
        st.write(f"**Allergies:** {', '.join(profile['allergies'])}")
    else:
        st.write("Koi allergy select nahi ki.")
    if profile.get("voice_enabled"):
        st.write("🔊 Voice: ON")
    st.divider()
    st.subheader("✨ GlucoGuard+ Features")
    st.caption("4 OpenAI models in one pipeline:")
    st.write("👁️ gpt-4o-mini — Label scanner")
    st.write("🧠 gpt-4o-mini — Verdict engine")
    st.write("🔍 gpt-4o-search-preview — Alternative finder")
    st.write("🔊 gpt-4o-mini-tts — Voice output")
    st.divider()
    if st.button("🍽️ Scan Khaana", use_container_width=True):
        st.session_state.page = "scan"
        st.rerun()
    if st.button("🩺 Edit Profile", use_container_width=True):
        st.session_state.page = "profile"
        st.rerun()

    # Fallback status indicator
    from src.config.settings import fallback_status
    fb = fallback_status()
    if any(fb.values()):
        st.divider()
        st.subheader("🛡️ Resilience Layer")
        st.caption("Multi-provider fallback active:")
        for provider, enabled in fb.items():
            icon = "✅" if enabled else "❌"
            st.write(f"{icon} {provider}")
        st.caption("OpenAI primary. Auto-fallback on rate limits.")


if st.session_state.page == "profile":
    show_profile_page()
else:
    show_scan_page()
