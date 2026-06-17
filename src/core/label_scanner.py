import base64
import json
from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, OPENAI_VISION_MODEL, GEMINI_API_KEY, GEMINI_VISION_MODEL
from src.core.knowledge_base import HIDDEN_SUGARS, ALLERGEN_MAP

SCAN_PROMPT = """You are looking at a photo of a packaged food product's label.

Read the label carefully and extract this information. Return ONLY a valid JSON
object (no markdown, no explanation, no code fences). The JSON must have exactly
these keys:

{
  "product_name": string or null,
  "brand": string or null,
  "serving_size": string or null,
  "servings_per_pack": number or null,
  "ingredients_raw": string or null,
  "ingredients_list": [string],
  "nutrition_per_serving": {
    "calories": number or null,
    "sugar_g": number or null,
    "sodium_g": number or null,
    "saturated_fat_g": number or null,
    "protein_g": number or null,
    "carbs_g": number or null
  },
  "nutrition_per_100g": {
    "calories": number or null,
    "sugar_g": number or null,
    "sodium_g": number or null,
    "saturated_fat_g": number or null
  },
  "allergen_statements": [string],
  "marketing_claims": [string],
  "label_language": string,
  "label_readability": string,
  "confidence": number
}

Rules:
- If a field is not visible on the label, use null (or empty list for arrays).
- Lowercase all ingredient names in ingredients_list.
- If the label is too blurry to read, return confidence < 0.3 and nulls for everything.
- Convert all sodium values to GRAMS (labels often say mg — divide by 1000).
- Do not invent values. Read only what is printed.
- For "sugar_g", include total sugars (added + naturally occurring) as printed.
- label_language: "english" | "urdu" | "bilingual" | "other"
- label_readability: "clear" | "partial" | "blurry"
- confidence: 0.0 to 1.0

Return the JSON now."""

def init_client():
    return OpenAI(api_key=OPENAI_API_KEY)

def scan_label_openai(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    client = init_client()
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64}"
    
    response = client.chat.completions.create(
        model=OPENAI_VISION_MODEL,
        messages=[
            {"role": "system", "content": "You are GlucoGuard+, a food label scanner for Pakistani consumers. You always respond with valid JSON only."},
            {"role": "user", "content": [
                {"type": "text", "text": SCAN_PROMPT},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]}
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
        max_tokens=1500
    )
    
    response_text = response.choices[0].message.content
    
    try:
        result = json.loads(response_text)
    except Exception as e:
        raise ValueError(f"Label parhne mein masla: GPT ne valid JSON nahi diya. Raw response: {response_text[:500]}")
        
    print(f"[label_scanner] Scan complete — confidence {result.get('confidence')}, {len(result.get('ingredients_list', []))} ingredients found")
    return result

def scan_label_gemini(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """Gemini fallback for label scanning."""
    import json
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    response = client.models.generate_content(
        model=GEMINI_VISION_MODEL,
        contents=[SCAN_PROMPT, image_part]
    )
    response_text = response.text.strip()

    # Strip markdown fences if present
    if response_text.startswith("```"):
        parts = response_text.split("```")
        response_text = parts[1] if len(parts) > 1 else response_text
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip("` \n")

    result = json.loads(response_text)
    print(f"[label_scanner] Gemini fallback scan complete — confidence {result.get('confidence')}")
    return result

def scan_label(image_bytes, mime_type="image/jpeg"):
    from src.core.fallback import with_fallback
    return with_fallback(scan_label_openai, scan_label_gemini, image_bytes, mime_type)
