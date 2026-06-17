import json
import streamlit as st
from PIL import Image
from io import BytesIO
from src.config.settings import OPENAI_TTS_MODEL, OPENAI_TTS_VOICE

def show_teach_mode(label_data, verdict, user_profile, image_bytes, mime_type):
    st.divider()
    st.subheader("🧠 Teach Mode — Dekhein AI ne kya kiya")
    st.caption("Yeh mode aap ko dikhata hai ke OpenAI ke models ne kis tarah socha. Learning ke liye behtareen.")

    # Expander 1: The image GPT-4o-mini saw
    with st.expander("1. GPT-4o-mini ne yeh image dekhi (vision)"):
        try:
            img = Image.open(BytesIO(image_bytes))
            st.image(img, caption="GPT-4o-mini ko bheji gayi photo", width=400)
        except Exception as e:
            st.error(f"Image render nahi hua: {e}")

    # Expander 2: The user profile + the system prompts sent to OpenAI
    with st.expander("2. User Profile + System Prompts"):
        st.write("**User Profile (jo verdict engine ko bheja gaya):**")
        st.code(json.dumps(user_profile, indent=2), language="json")

        st.write("**Health Verdict System Prompt Template:**")
        from src.core.health_verdict import VERDICT_PROMPT_TEMPLATE
        st.code(VERDICT_PROMPT_TEMPLATE, language="text")

        st.write("**Label Scanner System Prompt:**")
        from src.core.label_scanner import SCAN_PROMPT
        st.code(SCAN_PROMPT, language="text")

    # Expander 3: The raw label scan JSON (from gpt-4o-mini vision call)
    with st.expander("3. GPT-4o-mini se mila hua raw label scan (vision → JSON)"):
        st.code(json.dumps(label_data, indent=2, ensure_ascii=False), language="json")

    # Expander 4: The raw verdict JSON (from gpt-4o-mini text call)
    with st.expander("4. GPT-4o-mini se mila hua raw verdict (reasoning → JSON)"):
        st.code(json.dumps(verdict, indent=2, ensure_ascii=False), language="json")

    # Expander 5: Note about + features (added in Step 7)
    with st.expander("5. + Features"):
        st.info("Web search alternative aur TTS voice output ke inputs aur models ki information niche di gayi hai.")

    # Expander 6: + Feature 1 — Web search alternative
    if st.session_state.get("alternative"):
        with st.expander("6. + Feature: Web search alternative (gpt-4o-search-preview)"):
            st.write("**Search Prompt Template:**")
            from src.core.alternative_finder import ALTERNATIVE_PROMPT_TEMPLATE
            st.code(ALTERNATIVE_PROMPT_TEMPLATE, language="text")
            st.write("**Raw Alternative Response:**")
            st.code(json.dumps(st.session_state.alternative, indent=2, ensure_ascii=False), language="json")

    # Expander 7: + Feature 2 — TTS voice output
    if st.session_state.get("speech_text"):
        with st.expander("7. + Feature: Voice output (gpt-4o-mini-tts)"):
            st.write("**Speech Text (jo TTS ko bheja gaya):**")
            st.code(st.session_state.speech_text, language="text")
            st.write(f"**TTS Model:** {OPENAI_TTS_MODEL}")
            st.write(f"**Voice:** {OPENAI_TTS_VOICE}")
            if st.session_state.get("audio_bytes"):
                st.write(f"**Audio size:** {len(st.session_state.audio_bytes)} bytes")

    st.divider()
    if st.button("← Teach Mode Band Karein", type="primary"):
        st.session_state.show_teach_mode = False
        st.rerun()
