import json
from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, OPENAI_TEXT_MODEL, GROQ_API_KEY, GROQ_TEXT_MODEL
from src.core.knowledge_base import HIDDEN_SUGARS, ALLERGEN_MAP, DAILY_LIMITS

USER_PROFILE_SCHEMA = {
    "conditions": ["diabetes", "hypertension", "celiac", "pcos",
                   "high_cholesterol", "obesity", "none"],
    "allergies": list(ALLERGEN_MAP.keys()),
    "language": ["roman_urdu", "english", "urdu"],
}

VERDICT_PROMPT_TEMPLATE = """You are GlucoGuard+, a personalized food safety verdict engine for Pakistani consumers.
You will be given:
1. A user's health profile (conditions + allergies + language preference)
2. A structured label scan (JSON from the label scanner)
3. Reference data on hidden sugars and allergen aliases

Your job: produce a personalized verdict for THIS user eating THIS product.

Return ONLY a valid JSON object (no markdown, no explanation, no code fences).
The JSON must have exactly these keys:

{
  "verdict": "SAFE" | "MODERATE" | "AVOID",
  "verdict_color": "green" | "yellow" | "red",
  "verdict_reason_roman_urdu": string,
  "verdict_reason_english": string,
  "hidden_sugars_detected": [
    {
      "name": string,
      "type": "high_gi" | "added_sugar" | "sugar_alias",
      "concern_roman_urdu": string,
      "glycemic_index": number or null
    }
  ],
  "allergens_detected": [
    {
      "allergen": string,
      "matching_ingredient": string,
      "severity": "high" | "medium" | "low",
      "note_roman_urdu": string
    }
  ],
  "nutrition_analysis": {
    "sugar_g_per_serving": number or null,
    "sugar_pct_of_daily_limit": number or null,
    "sodium_g_per_serving": number or null,
    "sodium_pct_of_daily_limit": number or null,
    "calories_per_serving": number or null,
    "verdict_per_condition": {
      "diabetes": "safe" | "moderate" | "avoid" or null,
      "hypertension": "safe" | "moderate" | "avoid" or null,
      "celiac": "safe" | "moderate" | "avoid" or null,
      "pcos": "safe" | "moderate" | "avoid" or null,
      "high_cholesterol": "safe" | "moderate" | "avoid" or null
    }
  },
  "misleading_claims_flagged": [
    {
      "claim": string,
      "reality_roman_urdu": string
    }
  ],
  "healthier_alternative_roman_urdu": string,
  "healthier_alternative_english": string,
  "teachable_moment_roman_urdu": string
}

VERDICT LOGIC (follow strictly):
- AVOID (red) if: any user-listed allergen is detected in ingredients OR
                  sugar per serving > 75% of WHO daily limit (18.75g) AND user has diabetes OR
                  sodium per serving > 50% of daily limit (1g) AND user has hypertension
- MODERATE (yellow) if: hidden sugars detected but under AVOID threshold OR
                         sugar 25-75% of daily limit for diabetic users OR
                         sodium 25-50% of daily limit for hypertensive users
- SAFE (green) if: none of the above triggered

All Roman Urdu strings must be in plain Roman script (no Urdu script characters),
written the way a Pakistani would text — e.g. "Yeh aap ke liye munasib nahi"
NOT "یہ آپ کے لیے مناسب نہیں".

USER PROFILE:
{user_profile_json}

LABEL SCAN:
{label_data_json}

HIDDEN SUGARS REFERENCE (flag any of these if found in ingredients_list):
{hidden_sugars_json}

ALLERGEN REFERENCE (map ingredient names to allergen categories):
{allergen_map_json}

WHO DAILY LIMITS (adults):
{daily_limits_json}

Now produce the verdict JSON."""

def init_client():
    return OpenAI(api_key=OPENAI_API_KEY)

def generate_verdict_openai(label_data: dict, user_profile: dict) -> dict:
    client = init_client()
    
    prompt_text = VERDICT_PROMPT_TEMPLATE
    prompt_text = prompt_text.replace("{user_profile_json}", json.dumps(user_profile, indent=2))
    prompt_text = prompt_text.replace("{label_data_json}", json.dumps(label_data, indent=2))
    prompt_text = prompt_text.replace("{hidden_sugars_json}", json.dumps(HIDDEN_SUGARS, indent=2))
    prompt_text = prompt_text.replace("{allergen_map_json}", json.dumps(ALLERGEN_MAP, indent=2))
    prompt_text = prompt_text.replace("{daily_limits_json}", json.dumps(DAILY_LIMITS, indent=2))
    
    response = client.chat.completions.create(
        model=OPENAI_TEXT_MODEL,
        messages=[
            {"role": "system", "content": "You are GlucoGuard+, a personalized food safety verdict engine. You always respond with valid JSON only."},
            {"role": "user", "content": prompt_text}
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=2000
    )
    
    response_text = response.choices[0].message.content
    
    try:
        result = json.loads(response_text)
    except Exception as e:
        raise ValueError(f"Verdict generate nahi hua. Raw: {response_text[:500]}")
        
    print(f"[health_verdict] Verdict: {result['verdict']} — {len(result.get('hidden_sugars_detected', []))} hidden sugars, {len(result.get('allergens_detected', []))} allergens")
    return result

def generate_verdict_groq(label_data: dict, user_profile: dict) -> dict:
    """Groq fallback for verdict generation."""
    import json
    from openai import OpenAI

    # Build the same prompt as generate_verdict_openai
    prompt_text = VERDICT_PROMPT_TEMPLATE
    prompt_text = prompt_text.replace("{user_profile_json}", json.dumps(user_profile, indent=2))
    prompt_text = prompt_text.replace("{label_data_json}", json.dumps(label_data, indent=2))
    prompt_text = prompt_text.replace("{hidden_sugars_json}", json.dumps(HIDDEN_SUGARS, indent=2))
    prompt_text = prompt_text.replace("{allergen_map_json}", json.dumps(ALLERGEN_MAP, indent=2))
    prompt_text = prompt_text.replace("{daily_limits_json}", json.dumps(DAILY_LIMITS, indent=2))

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    response = client.chat.completions.create(
        model=GROQ_TEXT_MODEL,
        messages=[
            {"role": "system", "content": "You are GlucoGuard+, a personalized food safety verdict engine. You always respond with valid JSON only."},
            {"role": "user", "content": prompt_text}
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=2000
    )
    response_text = response.choices[0].message.content
    result = json.loads(response_text)
    print(f"[health_verdict] Groq fallback verdict: {result['verdict']}")
    return result

def generate_verdict(label_data, user_profile):
    from src.core.fallback import with_fallback
    return with_fallback(generate_verdict_openai, generate_verdict_groq, label_data, user_profile)
