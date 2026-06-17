import streamlit as st

CONDITION_OPTIONS = {
    "diabetes": "Diabetes / High Blood Sugar",
    "hypertension": "Hypertension / High Blood Pressure",
    "celiac": "Celiac Disease (Gluten Intolerance)",
    "pcos": "PCOS / Hormonal Imbalance",
    "high_cholesterol": "High Cholesterol",
    "obesity": "Obesity / Weight Management",
}

ALLERGY_OPTIONS = {
    "peanut": "Peanut",
    "tree_nut": "Tree Nuts (almond, cashew, walnut, etc.)",
    "gluten": "Gluten / Wheat",
    "dairy": "Dairy / Milk",
    "soy": "Soy",
    "egg": "Egg",
    "sesame": "Sesame",
    "seafood": "Seafood / Fish",
    "mustard": "Mustard",
    "sulphite": "Sulphites",
}

LANGUAGE_OPTIONS = {
    "roman_urdu": "Roman Urdu (e.g. 'Yeh khaana theek hai')",
    "english": "English",
    "urdu": "Urdu Script (اردو)",
}

def show_profile_page():
    st.title("🩺 Apni Sehat Ka Profile")
    st.caption("Yeh profile aap ki profile save karta hai. Har scan isi ke hisaab se personalized hoga.")
    st.divider()

    current = st.session_state.get("profile", {
        "conditions": ["none"],
        "allergies": ["none"],
        "language": "roman_urdu",
        "voice_enabled": False
    })

    st.subheader("Aap ki Conditions")
    st.caption("Jo bhi aap ko hai, tick karein. Agar kuch nahi, toh 'Koi condition nahi' select karein.")
    no_condition = st.checkbox("Koi condition nahi", value=("none" in current.get("conditions", [])))

    selected_conditions = []
    if not no_condition:
        for key, label in CONDITION_OPTIONS.items():
            if st.checkbox(label, value=(key in current.get("conditions", [])), key=f"cond_{key}"):
                selected_conditions.append(key)
    else:
        selected_conditions = ["none"]

    st.divider()
    st.subheader("Aap ki Allergies")
    st.caption("Jo bhi aap ko allergy hai, tick karein.")
    no_allergy = st.checkbox("Koi allergy nahi", value=("none" in current.get("allergies", [])))

    selected_allergies = []
    if not no_allergy:
        for key, label in ALLERGY_OPTIONS.items():
            if st.checkbox(label, value=(key in current.get("allergies", [])), key=f"all_{key}"):
                selected_allergies.append(key)
    else:
        selected_allergies = ["none"]

    st.divider()
    st.subheader("Zabaan (Language)")
    language = st.radio(
        "Verdict kis zabaan mein chahiye?",
        options=list(LANGUAGE_OPTIONS.keys()),
        format_func=lambda x: LANGUAGE_OPTIONS[x],
        index=list(LANGUAGE_OPTIONS.keys()).index(current.get("language", "roman_urdu")),
        horizontal=True
    )

    st.divider()
    st.subheader("🔊 GlucoGuard+ Voice Feature")
    st.caption("Anpadh logon ke liye: verdict awaaz mein sunayein (gpt-4o-mini-tts use hota hai).")
    voice_enabled = st.checkbox(
        "Verdict awaaz mein sunayein",
        value=current.get("voice_enabled", False),
        help="Yeh toggle on karne se har scan ke baad ek [▶ Play] button aayega jo verdict Roman Urdu mein sunaata hai."
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Profile Save Karein", type="primary", use_container_width=True):
            st.session_state.profile = {
                "conditions": selected_conditions,
                "allergies": selected_allergies,
                "language": language,
                "voice_enabled": voice_enabled
            }
            st.success("Profile save ho gaya! Ab Scan page par jaakar khaana scan karein.")
            st.session_state.page = "scan"
            st.rerun()
    with col2:
        if st.button("← Cancel", use_container_width=True):
            st.session_state.page = "scan"
            st.rerun()

    # Show a small summary at the bottom
    st.divider()
    st.subheader("Current Profile")
    profile_summary_col1, profile_summary_col2, profile_summary_col3 = st.columns(3)
    with profile_summary_col1:
        st.write("**Conditions:**")
        if selected_conditions == ["none"]:
            st.write("_None selected_")
        else:
            for c in selected_conditions:
                st.write(f"• {CONDITION_OPTIONS.get(c, c)}")
    with profile_summary_col2:
        st.write("**Allergies:**")
        if selected_allergies == ["none"]:
            st.write("_None selected_")
        else:
            for a in selected_allergies:
                st.write(f"• {ALLERGY_OPTIONS.get(a, a)}")
    with profile_summary_col3:
        st.write("**Voice:**")
        st.write("🔊 ON" if voice_enabled else "🔇 OFF")
        st.write(f"**Language:** {LANGUAGE_OPTIONS.get(language, language)}")
