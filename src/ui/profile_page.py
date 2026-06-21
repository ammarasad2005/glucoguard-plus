import streamlit as st

CONDITION_OPTIONS = {
    "diabetes": ("🩸", "Diabetes / High Blood Sugar"),
    "hypertension": ("❤️", "Hypertension / High Blood Pressure"),
    "celiac": ("🌾", "Celiac Disease (Gluten Intolerance)"),
    "pcos": (" Hormonal", "PCOS / Hormonal Imbalance"),
    "high_cholesterol": ("🫀", "High Cholesterol"),
    "obesity": ("⚖️", "Obesity / Weight Management"),
}

ALLERGY_OPTIONS = {
    "peanut": ("🥜", "Peanut"),
    "tree_nut": ("🌰", "Tree Nuts (almond, cashew, walnut)"),
    "gluten": ("🌾", "Gluten / Wheat"),
    "dairy": ("🥛", "Dairy / Milk"),
    "soy": ("🌱", "Soy"),
    "egg": ("🥚", "Egg"),
    "sesame": ("⚪", "Sesame"),
    "seafood": ("🐟", "Seafood / Fish"),
    "mustard": ("yellow", "Mustard"),
    "sulphite": ("🍷", "Sulphites"),
}

LANGUAGE_OPTIONS = {
    "roman_urdu": "Roman Urdu (e.g. 'Yeh khaana theek hai')",
    "english": "English",
    "urdu": "Urdu Script (اردو)",
}


def show_profile_page():
    # Use a centered column
    col_left, main_col, col_right = st.columns([1, 6, 1])
    with main_col:
        st.markdown("""
        <div class="gg-hero gg-fade-in" style="background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);">
            <h1>🩺 Apni Sehat Ka Profile</h1>
            <p>Yeh profile har scan ko personalize karta hai. Aap ki conditions aur allergies ke hisaab se verdict milega.</p>
        </div>
        """, unsafe_allow_html=True)

        current = st.session_state.get("profile", {
            "conditions": ["none"],
            "allergies": ["none"],
            "language": "roman_urdu",
            "voice_enabled": False
        })

        # === CONDITIONS ===
        st.markdown("""
        <div class="gg-section gg-fade-in">
            <h3 class="gg-section-title">🩸 Aap ki Conditions</h3>
            <p style="color: var(--gg-text-muted); font-size: 0.9rem; margin: 0 0 1rem 0;">Jo bhi aap ko hai, tick karein. Agar kuch nahi, toh 'Koi condition nahi' select karein.</p>
        </div>
        """, unsafe_allow_html=True)

        no_condition = st.checkbox("✅ Koi condition nahi", value=("none" in current.get("conditions", [])))

        selected_conditions = []
        if not no_condition:
            # Use a 2-column grid for conditions
            cond_cols = st.columns(2)
            for i, (key, (icon, label)) in enumerate(CONDITION_OPTIONS.items()):
                with cond_cols[i % 2]:
                    if st.checkbox(f"{icon} {label}", value=(key in current.get("conditions", [])), key=f"cond_{key}"):
                        selected_conditions.append(key)
        else:
            selected_conditions = ["none"]

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        # === ALLERGIES ===
        st.markdown("""
        <div class="gg-section gg-fade-in">
            <h3 class="gg-section-title">⚠️ Aap ki Allergies</h3>
            <p style="color: var(--gg-text-muted); font-size: 0.9rem; margin: 0 0 1rem 0;">Jo bhi aap ko allergy hai, tick karein.</p>
        </div>
        """, unsafe_allow_html=True)

        no_allergy = st.checkbox("✅ Koi allergy nahi", value=("none" in current.get("allergies", [])))

        selected_allergies = []
        if not no_allergy:
            allergy_cols = st.columns(2)
            for i, (key, (icon, label)) in enumerate(ALLERGY_OPTIONS.items()):
                with allergy_cols[i % 2]:
                    if st.checkbox(f"{icon} {label}", value=(key in current.get("allergies", [])), key=f"all_{key}"):
                        selected_allergies.append(key)
        else:
            selected_allergies = ["none"]

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        # === LANGUAGE ===
        st.markdown("""
        <div class="gg-section gg-fade-in">
            <h3 class="gg-section-title">🌐 Zabaan (Language)</h3>
        </div>
        """, unsafe_allow_html=True)
        language = st.radio(
            "Verdict kis zabaan mein chahiye?",
            options=list(LANGUAGE_OPTIONS.keys()),
            format_func=lambda x: LANGUAGE_OPTIONS[x],
            index=list(LANGUAGE_OPTIONS.keys()).index(current.get("language", "roman_urdu")),
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        # === VOICE ===
        st.markdown("""
        <div class="gg-section gg-fade-in">
            <h3 class="gg-section-title">🔊 GlucoGuard+ Voice Feature</h3>
            <p style="color: var(--gg-text-muted); font-size: 0.9rem; margin: 0 0 1rem 0;">
                Anpadh logon ke liye: verdict awaaz mein sunayein (gpt-4o-mini-tts use hota hai, edge-tts fallback).
            </p>
        </div>
        """, unsafe_allow_html=True)

        voice_enabled = st.toggle(
            "Verdict awaaz mein sunayein",
            value=current.get("voice_enabled", False),
            help="Yeh toggle on karne se har scan ke baad ek [▶ Play] button aayega jo verdict Roman Urdu mein sunaata hai."
        )

        if voice_enabled:
            st.success("🔊 Voice enabled! Har scan ke baad awaaz sunegi.")
        else:
            st.caption("🔇 Voice off — sirf text verdict milega.")

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # === SAVE BUTTONS ===
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("💾 Profile Save Karein", type="primary", use_container_width=True):
                st.session_state.profile = {
                    "conditions": selected_conditions,
                    "allergies": selected_allergies,
                    "language": language,
                    "voice_enabled": voice_enabled
                }
                st.success("✅ Profile save ho gaya! Scan page par jaakar khaana scan karein.")
                st.balloons()
                import time
                time.sleep(1.5)
                st.session_state.page = "scan"
                st.rerun()
        with col2:
            if st.button("← Cancel", use_container_width=True):
                st.session_state.page = "scan"
                st.rerun()
        with col3:
            pass

        # === PROFILE SUMMARY ===
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="gg-section gg-fade-in">
            <h3 class="gg-section-title">📋 Current Profile Summary</h3>
        </div>
        """, unsafe_allow_html=True)

        sum1, sum2, sum3, sum4 = st.columns(4)
        with sum1:
            st.markdown("**Conditions:**")
            if selected_conditions == ["none"]:
                st.caption("_None_")
            else:
                for c in selected_conditions:
                    icon, label = CONDITION_OPTIONS.get(c, ("•", c))
                    st.write(f"{icon} {label}")
        with sum2:
            st.markdown("**Allergies:**")
            if selected_allergies == ["none"]:
                st.caption("_None_")
            else:
                for a in selected_allergies:
                    icon, label = ALLERGY_OPTIONS.get(a, ("•", a))
                    st.write(f"{icon} {label}")
        with sum3:
            st.markdown("**Voice:**")
            if voice_enabled:
                st.write("🔊 ON")
            else:
                st.write("🔇 OFF")
        with sum4:
            st.markdown("**Language:**")
            st.write(LANGUAGE_OPTIONS.get(language, language))
