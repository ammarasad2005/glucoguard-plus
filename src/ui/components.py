import streamlit as st

def show_header():
    st.title("🛡️ GlucoGuard+")
    st.caption("Apne khaane ka guard banayein. Awaaz mein. Roman Urdu mein. Pakistan ke 33M diabetes patients ke liye.")
    st.divider()

def show_error(message: str):
    if message:
        st.error(message)
        if st.button("Theek karein"):
            st.session_state.error = None
            st.rerun()

def show_verdict_card(verdict: dict):
    verdict_text = verdict.get("verdict", "UNKNOWN")
    color = verdict.get("verdict_color", "green")
    reason = verdict.get("verdict_reason_roman_urdu", "")
    
    body = f"### Verdict: {verdict_text}\n\n{reason}"
    if color == "green":
        st.success(body)
    elif color == "yellow":
        st.warning(body)
    else:
        st.error(body)

def show_hidden_sugars(sugars: list):
    if not sugars:
        st.info("Koi chhupi hui cheeni nahi mili ✅")
        return
        
    st.subheader("❗ Chhupi hui cheeniyan")
    for sugar in sugars:
        name = sugar.get("name", "Unknown Sugar")
        concern = sugar.get("concern_roman_urdu", "")
        gi = sugar.get("glycemic_index")
        
        with st.expander(name):
            st.write(concern)
            if gi is not None:
                st.write(f"**Glycemic Index (GI):** {gi}")

def show_allergens(allergens: list):
    if not allergens:
        st.info("Aap ki allergy ka koi ingredient nahi mila ✅")
        return
        
    st.subheader("⚠️ Allergy Alert")
    for allergen in allergens:
        category = allergen.get("allergen", "").upper()
        matching = allergen.get("matching_ingredient", "")
        note = allergen.get("note_roman_urdu", "")
        st.error(f"**{category}**: {matching} — {note}")

def show_nutrition(analysis: dict):
    sugar_g = analysis.get("sugar_g_per_serving")
    sugar_pct = analysis.get("sugar_pct_of_daily_limit")
    sodium_g = analysis.get("sodium_g_per_serving")
    sodium_pct = analysis.get("sodium_pct_of_daily_limit")
    calories = analysis.get("calories_per_serving")
    
    sugar_val = f"{sugar_g}g" if sugar_g is not None else "N/A"
    sugar_delta = f"-{100 - sugar_pct}% headroom" if sugar_pct is not None else None
    
    sodium_val = f"{sodium_g}g" if sodium_g is not None else "N/A"
    sodium_delta = f"-{100 - sodium_pct}% headroom" if sodium_pct is not None else None
    
    cal_val = f"{calories} kcal" if calories is not None else "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Cheeni (per serving)", value=sugar_val, delta=sugar_delta)
    with col2:
        st.metric(label="Sodium (per serving)", value=sodium_val, delta=sodium_delta)
    with col3:
        st.metric(label="Calories (per serving)", value=cal_val)

def show_alternative(verdict: dict):
    st.subheader("💡 Behtar Alternative")
    st.success(verdict.get("healthier_alternative_roman_urdu", "Alternative details not provided."))
    st.info(verdict.get("teachable_moment_roman_urdu", ""))

def show_misleading_claims(claims: list):
    if not claims:
        return
        
    st.subheader("🏷️ Marketing Claims ki haqeeqat")
    for claim in claims:
        name = claim.get("claim", "")
        reality = claim.get("reality_roman_urdu", "")
        st.warning(f"**{name}**: {reality}")
