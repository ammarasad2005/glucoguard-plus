import streamlit as st
from src.ui.components import (
    show_header,
    show_error,
    show_verdict_card,
    show_hidden_sugars,
    show_allergens,
    show_nutrition,
    show_misleading_claims,
    show_alternative
)
from src.core.label_scanner import scan_label
from src.core.health_verdict import generate_verdict

def show_scan_page():
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
        return  # don't render the rest of the scan page while teach mode is on
        
    if st.session_state.get("error"):
        show_error(st.session_state.error)
        
    uploaded_file = st.file_uploader("Apne khaane ki packing ki photo upload karein", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Aap ki upload ki gayi photo", width=300)
        
        if st.button("🛡️ Guard Karein", type="primary"):
            try:
                # 1. Scanner Spinner
                with st.spinner("Label parh raha hoon... (gpt-4o-mini)"):
                    image_bytes = uploaded_file.read()
                    mime_type = uploaded_file.type if uploaded_file.type else "image/jpeg"
                    label_data = scan_label(image_bytes, mime_type)
                    
                # 2. Verdict Spinner
                with st.spinner("Sehat ka hisaab lagaa raha hoon... (gpt-4o-mini)"):
                    user_profile = st.session_state.get("profile", {"conditions": ["none"], "allergies": ["none"], "language": "roman_urdu", "voice_enabled": False})
                    # Normalize empty selections to "none" so the verdict engine doesn't think no profile is set
                    if not user_profile.get("conditions"):
                        user_profile["conditions"] = ["none"]
                    if not user_profile.get("allergies"):
                        user_profile["allergies"] = ["none"]
                    
                    verdict = generate_verdict(label_data, user_profile)

                # 3. Alternative Spinner
                with st.spinner("Behtar alternative dhoondh raha hoon... (gpt-4o-search-preview)"):
                    from src.core.alternative_finder import find_alternative
                    alternative = find_alternative(label_data, verdict, user_profile)

                # 4. Voice Spinner (only if voice_enabled)
                audio_bytes = None
                speech_text = None
                if user_profile.get("voice_enabled"):
                    with st.spinner("Awaaz tayyar kar raha hoon... (gpt-4o-mini-tts)"):
                        try:
                            from src.core.voice_output import build_speech_text, generate_voice
                            speech_text = build_speech_text(verdict, alternative)
                            audio_bytes = generate_voice(speech_text)
                        except Exception as tts_err:
                            print(f"[scan_page] TTS generation failed: {tts_err}")
                            audio_bytes = None

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
                
    # If verdict results exist in session state, display them
    if st.session_state.get("verdict") is not None:
        verdict = st.session_state.verdict
        label_data = st.session_state.label_data
        
        show_verdict_card(verdict)
        
        with st.expander("📋 Product Details"):
            st.write(f"**Product Name:** {label_data.get('product_name')}")
            st.write(f"**Brand:** {label_data.get('brand')}")
            st.write(f"**Serving Size:** {label_data.get('serving_size')}")
            st.write(f"**Servings per Pack:** {label_data.get('servings_per_pack')}")
            st.write(f"**Raw Ingredients:** {label_data.get('ingredients_raw')}")
            
        show_hidden_sugars(verdict.get("hidden_sugars_detected", []))
        show_allergens(verdict.get("allergens_detected", []))
        show_nutrition(verdict.get("nutrition_analysis", {}))
        show_misleading_claims(verdict.get("misleading_claims_flagged", []))
        show_alternative(verdict)
        
        # + Feature 1: Live web search alternative (overrides the LLM-suggested one if found)
        if st.session_state.get("alternative"):
            alt = st.session_state.alternative
            if alt.get("alternative_product"):
                st.subheader("🔍 Behtar Alternative (Live Web Search)")
                st.success(f"**{alt['alternative_product']}** by {alt.get('alternative_brand', 'N/A')}\n\n{alt.get('why_better_roman_urdu', '')}")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if alt.get("estimated_price_pkr"):
                        st.metric("Keemat (PKR)", f"Rs. {alt['estimated_price_pkr']}")
                    else:
                        st.metric("Keemat", "N/A")
                with col_b:
                    stores = alt.get("where_to_buy", [])
                    st.metric("Kahan milega", ", ".join(stores[:2]) if stores else "N/A")
                with col_c:
                    if alt.get("online_link"):
                        st.markdown(f"[🛒 Online Order]({alt['online_link']})")
                    else:
                        st.write("")
                sources = alt.get("search_sources", [])
                if sources:
                    with st.expander(f"📚 Web search sources ({len(sources)})"):
                        for s in sources[:5]:
                            st.write(f"• {s}")
            else:
                st.info("Live web search mein koi specific alternative nahi mila. LLM suggestion upar dekhein.")

        # + Feature 2: Voice output (TTS)
        if st.session_state.get("audio_bytes"):
            st.subheader("🔊 Suniye — Verdict Awaaz Mein")
            st.caption("Yeh GlucoGuard+ ka '+' feature hai — 40% anpadh logon ke liye.")
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
            with st.expander("📝 Awaaz mein kya kaha gaya (transcript)"):
                st.write(st.session_state.get("speech_text", ""))
        elif st.session_state.get("profile", {}).get("voice_enabled"):
            st.info("Voice on hai lekin TTS fail hua. Text verdict upar dekhein.")
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Dusra Khaana Guard Karein"):
                st.session_state.verdict = None
                st.session_state.label_data = None
                st.session_state.scanned_image = None
                st.session_state.scanned_image_mime = None
                st.rerun()
        with col2:
            if st.button("🧠 Mujhe Samjha Dein (Teach Mode)"):
                st.session_state.show_teach_mode = True
                st.rerun()
