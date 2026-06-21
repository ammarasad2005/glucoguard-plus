import streamlit as st
from src.ui.theme import hero, stats_bar, verdict_card, hidden_sugar_pills, allergen_badges, alternative_card, voice_card, step_indicator


def show_header():
    """Render the hero header + stats bar."""
    hero()
    stats_bar()


def show_step_indicator(current_step: int = 0):
    """Show the 4-step pipeline progress."""
    step_indicator(current_step)


def show_error(message: str):
    if message:
        st.error(f"⚠️ {message}")
        if st.button("✓ Theek karein", type="primary"):
            st.session_state.error = None
            st.rerun()


def show_verdict_card(verdict: dict):
    """Render the polished verdict card."""
    verdict_card(verdict)


def show_hidden_sugars(sugars: list):
    """Render hidden sugars as pills."""
    hidden_sugar_pills(sugars)


def show_allergens(allergens: list):
    """Render allergens as badges."""
    allergen_badges(allergens)


def show_nutrition(analysis: dict):
    """Render nutrition metrics in a styled card."""
    sugar_g = analysis.get("sugar_g_per_serving")
    sugar_pct = analysis.get("sugar_pct_of_daily_limit")
    sodium_g = analysis.get("sodium_g_per_serving")
    sodium_pct = analysis.get("sodium_pct_of_daily_limit")
    calories = analysis.get("calories_per_serving")

    st.markdown("""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">📊 Sehat Ka Hisab (per serving)</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        sugar_val = f"{sugar_g}g" if sugar_g is not None else "N/A"
        if sugar_pct is not None:
            sugar_delta = f"{int(sugar_pct)}% of daily limit"
            sugar_delta_color = "inverse" if sugar_pct > 75 else ("off" if sugar_pct > 25 else "normal")
        else:
            sugar_delta = None
            sugar_delta_color = "off"
        st.metric("🍯 Cheeni", sugar_val, delta=sugar_delta, delta_color=sugar_delta_color if sugar_delta else "off")
    with col2:
        sodium_val = f"{sodium_g}g" if sodium_g is not None else "N/A"
        if sodium_pct is not None:
            sodium_delta = f"{int(sodium_pct)}% of daily limit"
            sodium_delta_color = "inverse" if sodium_pct > 75 else ("off" if sodium_pct > 25 else "normal")
        else:
            sodium_delta = None
            sodium_delta_color = "off"
        st.metric("🧂 Sodium", sodium_val, delta=sodium_delta, delta_color=sodium_delta_color if sodium_delta else "off")
    with col3:
        cal_val = f"{calories}" if calories is not None else "N/A"
        st.metric("🔥 Calories", cal_val, delta="kcal" if calories is not None else None, delta_color="off")


def show_alternative(verdict: dict):
    """Render the LLM-suggested alternative."""
    st.markdown("""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">💡 AI Suggested Alternative</h3>
    </div>
    """, unsafe_allow_html=True)
    alt_text = verdict.get("healthier_alternative_roman_urdu", "Alternative details not provided.")
    teachable = verdict.get("teachable_moment_roman_urdu", "")
    st.success(alt_text)
    if teachable:
        st.info(f"📚 **Did you know?** {teachable}")


def show_live_alternative(alt: dict):
    """Render the live web search alternative card."""
    if alt and alt.get("alternative_product"):
        alternative_card(alt)
    elif alt:
        st.info("Live web search mein koi specific alternative nahi mila. AI suggestion upar dekhein.")


def show_voice_player(audio_bytes: bytes, speech_text: str = ""):
    """Render the styled voice card with audio player."""
    if audio_bytes:
        voice_card()
        st.audio(audio_bytes, format="audio/mp3")
        if speech_text:
            with st.expander("📝 Transcript — Awaaz mein kya kaha gaya"):
                st.write(speech_text)


def show_misleading_claims(claims: list):
    """Render misleading claims in a styled card."""
    if not claims:
        return

    st.markdown("""
    <div class="gg-section gg-fade-in">
        <h3 class="gg-section-title">🏷️ Marketing Claims ki Haqeeqat</h3>
    </div>
    """, unsafe_allow_html=True)
    for claim in claims:
        name = claim.get("claim", "")
        reality = claim.get("reality_roman_urdu", "")
        st.warning(f"**\"{name}\"** — {reality}")


def show_product_details(label_data: dict):
    """Render product details in a styled expander."""
    with st.expander("📋 Product Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Product:** {label_data.get('product_name', 'N/A')}")
            st.write(f"**Brand:** {label_data.get('brand', 'N/A')}")
            st.write(f"**Serving:** {label_data.get('serving_size', 'N/A')}")
        with col2:
            st.write(f"**Servings/pack:** {label_data.get('servings_per_pack', 'N/A')}")
            st.write(f"**Language:** {label_data.get('label_language', 'N/A')}")
            st.write(f"**Confidence:** {label_data.get('confidence', 'N/A')}")

        ingredients = label_data.get("ingredients_raw", "")
        if ingredients:
            st.write(f"**Raw Ingredients:** {ingredients}")


def show_action_buttons():
    """Render the bottom action buttons."""
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔁 Dusra Khaana", use_container_width=True):
            st.session_state.verdict = None
            st.session_state.label_data = None
            st.session_state.alternative = None
            st.session_state.audio_bytes = None
            st.session_state.speech_text = None
            st.session_state.scanned_image = None
            st.session_state.scanned_image_mime = None
            st.session_state.show_teach_mode = False
            st.rerun()
    with col2:
        if st.button("🧠 Teach Mode", use_container_width=True):
            st.session_state.show_teach_mode = True
            st.rerun()
    with col3:
        # Empty placeholder for alignment
        pass
