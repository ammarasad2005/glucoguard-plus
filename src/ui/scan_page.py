import streamlit as st
from src.ui.components import (
    show_header,
    show_step_indicator,
    show_error,
    show_verdict_card,
    show_hidden_sugars,
    show_allergens,
    show_nutrition,
    show_misleading_claims,
    show_alternative,
    show_live_alternative,
    show_voice_player,
    show_product_details,
    show_action_buttons,
)
from src.core.label_scanner import scan_label
from src.core.health_verdict import generate_verdict


def show_scan_page():
    # Use a centered column for content (max 900px wide)
    col_left, main_col, col_right = st.columns([1, 6, 1])
    with main_col:
        show_header()

        # Teach mode overlay
        if st.session_state.get("show_teach_mode") and st.session_state.get("verdict"):
            from src.ui.teach_mode import show_teach_mode
            show_teach_mode(
                label_data=st.session_state.label_data,
                verdict=st.session_state.verdict,
                user_profile=st.session_state.profile,
                image_bytes=st.session_state.scanned_image,
                mime_type=st.session_state.scanned_image_mime
            )
            return

        if st.session_state.get("error"):
            show_error(st.session_state.error)

        # === UPLOAD SECTION ===
        if not st.session_state.get("verdict"):
            st.markdown("### 📸 Apne khaane ki packing ki photo upload karein")
            st.caption("JPG, PNG, ya WebP — label saaf dikhna chahiye")

            uploaded_file = st.file_uploader(
                "Photo drag karein ya click karke select karein",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed"
            )

            if uploaded_file is not None:
                # Show preview in a nice layout
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    st.image(uploaded_file, caption="Upload ki gayi photo", use_container_width=True)
                with col_info:
                    st.markdown("#### ✅ Photo ready")
                    st.write("• Image loaded successfully")
                    st.write("• Click below to start the scan")
                    st.write("• 4 AI models will run in sequence (~15-25 sec)")

                    if st.button("🛡️ Guard Karein", type="primary", use_container_width=True):
                        run_scan_pipeline(uploaded_file)
        else:
            # === RESULTS SECTION ===
            show_results()

        # Action buttons at the bottom (only if results exist)
        if st.session_state.get("verdict"):
            show_action_buttons()


def run_scan_pipeline(uploaded_file):
    """Run the 4-step scan pipeline with progress indicators."""
    try:
        # Show step indicator
        show_step_indicator(0)

        # Step 1: Scanner
        with st.spinner("👁️ Label parh raha hoon..."):
            image_bytes = uploaded_file.read()
            mime_type = uploaded_file.type if uploaded_file.type else "image/jpeg"
            label_data = scan_label(image_bytes, mime_type)

        show_step_indicator(1)

        # Step 2: Verdict
        with st.spinner("🧠 Sehat ka hisaab lagaa raha hoon..."):
            user_profile = st.session_state.get("profile", {"conditions": ["none"], "allergies": ["none"], "language": "roman_urdu", "voice_enabled": False})
            if not user_profile.get("conditions"):
                user_profile["conditions"] = ["none"]
            if not user_profile.get("allergies"):
                user_profile["allergies"] = ["none"]
            verdict = generate_verdict(label_data, user_profile)

        show_step_indicator(2)

        # Step 3: Alternative
        with st.spinner("🔍 Behtar alternative dhoondh raha hoon..."):
            from src.core.alternative_finder import find_alternative
            alternative = find_alternative(label_data, verdict, user_profile)

        show_step_indicator(3)

        # Step 4: Voice (only if enabled)
        audio_bytes = None
        speech_text = None
        if user_profile.get("voice_enabled"):
            with st.spinner("🔊 Awaaz tayyar kar raha hoon..."):
                try:
                    from src.core.voice_output import build_speech_text, generate_voice
                    speech_text = build_speech_text(verdict, alternative)
                    audio_bytes = generate_voice(speech_text)
                except Exception as tts_err:
                    print(f"[scan_page] TTS generation failed: {tts_err}")
                    audio_bytes = None

        show_step_indicator(4)

        # Store all in session state
        st.session_state.label_data = label_data
        st.session_state.verdict = verdict
        st.session_state.alternative = alternative
        st.session_state.audio_bytes = audio_bytes
        st.session_state.speech_text = speech_text
        st.session_state.scanned_image = image_bytes
        st.session_state.scanned_image_mime = mime_type
        st.rerun()

    except Exception as e:
        st.session_state.error = str(e)
        st.rerun()


def show_results():
    """Render the full results page."""
    verdict = st.session_state.verdict
    label_data = st.session_state.label_data

    # Verdict card (the hero)
    show_verdict_card(verdict)

    # Product details
    show_product_details(label_data)

    # Hidden sugars
    show_hidden_sugars(verdict.get("hidden_sugars_detected", []))

    # Allergens
    show_allergens(verdict.get("allergens_detected", []))

    # Nutrition metrics
    show_nutrition(verdict.get("nutrition_analysis", {}))

    # Misleading claims
    show_misleading_claims(verdict.get("misleading_claims_flagged", []))

    # AI-suggested alternative
    show_alternative(verdict)

    # Live web search alternative
    if st.session_state.get("alternative"):
        show_live_alternative(st.session_state.alternative)

    # Voice player
    if st.session_state.get("audio_bytes"):
        show_voice_player(st.session_state.audio_bytes, st.session_state.get("speech_text", ""))
    elif st.session_state.get("profile", {}).get("voice_enabled"):
        st.info("🔊 Voice on hai lekin TTS fail hua. Text verdict upar dekhein.")
