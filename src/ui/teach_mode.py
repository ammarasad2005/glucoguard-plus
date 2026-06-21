import json
import streamlit as st
from PIL import Image
from io import BytesIO
from src.config.settings import OPENAI_TTS_MODEL, OPENAI_TTS_VOICE


def show_teach_mode(label_data, verdict, user_profile, image_bytes, mime_type):
    # Centered column layout
    col_left, main_col, col_right = st.columns([1, 6, 1])
    with main_col:
        st.markdown("""
        <div class="gg-hero gg-fade-in" style="background: linear-gradient(135deg, #6B21A8 0%, #4C1D95 100%);">
            <h1>🧠 Teach Mode</h1>
            <p>Dekhein AI ne kis tarah socha. Har model call ka prompt aur raw response niche di gaya hai.</p>
            <span class="gg-badge">📚 Learning mode · Open Innovation bonus</span>
        </div>
        """, unsafe_allow_html=True)

        # Expander 1: The image GPT-4o-mini saw
        with st.expander("1. 👁️ GPT-4o-mini ne yeh image dekhi (vision)", expanded=False):
            try:
                img = Image.open(BytesIO(image_bytes))
                st.image(img, caption="GPT-4o-mini ko bheji gayi photo", width=400)
            except Exception as e:
                st.error(f"Image render nahi hua: {e}")

        # Expander 2: The user profile + the system prompts
        with st.expander("2. 📝 User Profile + System Prompts", expanded=False):
            st.markdown("**User Profile (jo verdict engine ko bheja gaya):**")
            st.code(json.dumps(user_profile, indent=2), language="json")

            st.markdown("**Health Verdict System Prompt Template:**")
            from src.core.health_verdict import VERDICT_PROMPT_TEMPLATE
            st.code(VERDICT_PROMPT_TEMPLATE, language="text")

            st.markdown("**Label Scanner System Prompt:**")
            from src.core.label_scanner import SCAN_PROMPT
            st.code(SCAN_PROMPT, language="text")

        # Expander 3: The raw label scan JSON
        with st.expander("3. 📊 Raw Label Scan (vision → JSON)", expanded=False):
            st.code(json.dumps(label_data, indent=2, ensure_ascii=False), language="json")

        # Expander 4: The raw verdict JSON
        with st.expander("4. ⚖️ Raw Verdict (reasoning → JSON)", expanded=False):
            st.code(json.dumps(verdict, indent=2, ensure_ascii=False), language="json")

        # Expander 5: Web search alternative
        if st.session_state.get("alternative"):
            with st.expander("5. 🔍 Web Search Alternative (gpt-4o-search-preview → Tavily+Groq fallback)", expanded=False):
                st.markdown("**Search Prompt Template:**")
                from src.core.alternative_finder import ALTERNATIVE_PROMPT_TEMPLATE
                st.code(ALTERNATIVE_PROMPT_TEMPLATE, language="text")
                st.markdown("**Raw Alternative Response:**")
                st.code(json.dumps(st.session_state.alternative, indent=2, ensure_ascii=False), language="json")

        # Expander 6: TTS voice output
        if st.session_state.get("speech_text"):
            with st.expander("6. 🔊 Voice Output (gpt-4o-mini-tts → edge-tts fallback)", expanded=False):
                st.markdown("**Speech Text (jo TTS ko bheja gaya):**")
                st.code(st.session_state.speech_text, language="text")
                st.markdown(f"**Primary TTS Model:** `{OPENAI_TTS_MODEL}`")
                st.markdown(f"**Primary Voice:** `{OPENAI_TTS_VOICE}`")
                st.markdown("**Fallback:** `edge-tts` (Microsoft neural voices, no API key, unlimited)")
                if st.session_state.get("audio_bytes"):
                    st.markdown(f"**Audio size:** {len(st.session_state.audio_bytes):,} bytes")

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        if st.button("← Teach Mode Band Karein", type="primary", use_container_width=True):
            st.session_state.show_teach_mode = False
            st.rerun()
