from openai import OpenAI
from src.config.settings import (
    OPENAI_API_KEY, OPENAI_SEARCH_MODEL, GROQ_API_KEY, GROQ_TEXT_MODEL,
    TAVILY_API_KEY, GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX
)
import requests
import json

ALTERNATIVE_PROMPT_TEMPLATE = """You are GlucoGuard+, a health product finder for Pakistani consumers.

The user just scanned a food product that was verdict'd as {verdict} for their health profile.

PRODUCT SCANNED: {product_name} by {brand}
USER CONDITIONS: {conditions}
USER ALLERGIES: {allergies}
VERDICT REASON: {verdict_reason}

Your job: search the web for ONE specific healthier alternative product that is:
1. Actually available to buy in Pakistan (search Naheed, Chase Up, Carrefour, Imtiaz, Al-Fatah, Anees Supermarket, Yadley, Hashim Supermarket, or online at naheed.com, chaseup.com.pk, daraz.pk)
2. Safer for the user's specific conditions and allergies
3. From a real brand (not "eat fruit" or "drink water" — find an actual packaged product)

Search the web now. Then return ONLY a valid JSON object with these keys:

{{
  "alternative_product": string,
  "alternative_brand": string,
  "why_better_roman_urdu": string,
  "where_to_buy": [string],
  "estimated_price_pkr": number or null,
  "online_link": string or null,
  "search_sources": [string]
}}

Rules:
- The alternative must be a real product findable on Pakistani store websites.
- why_better_roman_urdu: 1-2 sentences in Roman Urdu (no Urdu script).
- where_to_buy: list of Pakistani store names where it's available.
- estimated_price_pkr: integer PKR price if found, else null.
- online_link: a real URL if found, else null.
- search_sources: list of URLs the search model used.
- If you cannot find a real Pakistani alternative, return alternative_product=null and explain in why_better_roman_urdu what to look for.

Return the JSON now.
"""

def init_client():
    return OpenAI(api_key=OPENAI_API_KEY)

def find_alternative_openai(label_data: dict, verdict: dict, user_profile: dict) -> dict:
    """Find a real, healthier alternative product available in Pakistan via web search."""
    client = init_client()

    prompt = ALTERNATIVE_PROMPT_TEMPLATE.format(
        verdict=verdict.get("verdict", "UNKNOWN"),
        product_name=label_data.get("product_name") or "this product",
        brand=label_data.get("brand") or "unknown brand",
        conditions=", ".join(user_profile.get("conditions", [])) or "none",
        allergies=", ".join(user_profile.get("allergies", [])) or "none",
        verdict_reason=verdict.get("verdict_reason_english", "no reason provided")
    )

    try:
        response = client.chat.completions.create(
            model=OPENAI_SEARCH_MODEL,
            messages=[
                {"role": "system", "content": "You are GlucoGuard+, a Pakistani health product finder. You search the web and return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            # Note: search-preview model does NOT support response_format — it returns text with citations
            max_tokens=1000
        )
        response_text = response.choices[0].message.content.strip()

        # The search-preview model may wrap JSON in markdown or add citations.
        # Try to extract a JSON object from the response.
        import json
        import re

        # Try direct parse first
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to find a JSON block in the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    # Fall back to a stub result with the raw text
                    result = {
                        "alternative_product": None,
                        "alternative_brand": None,
                        "why_better_roman_urdu": "Web search se valid response nahi mila. LLM alternative dekh lein.",
                        "where_to_buy": [],
                        "estimated_price_pkr": None,
                        "online_link": None,
                        "search_sources": [],
                        "_raw_response": response_text[:1000]
                    }
            else:
                result = {
                    "alternative_product": None,
                    "alternative_brand": None,
                    "why_better_roman_urdu": "Web search se valid response nahi mila.",
                    "where_to_buy": [],
                    "estimated_price_pkr": None,
                    "online_link": None,
                    "search_sources": [],
                    "_raw_response": response_text[:1000]
                }

        print(f"[alternative_finder] Alternative found: {result.get('alternative_product')} — sources: {len(result.get('search_sources', []))}")
        return result

    except Exception as e:
        print(f"[alternative_finder] Error: {e}")
        raise e

def find_alternative_tavily(label_data: dict, verdict: dict, user_profile: dict) -> dict:
    """Tavily + Groq fallback for finding real alternatives."""
    product_name = label_data.get("product_name") or "this product"
    brand = label_data.get("brand") or ""
    conditions = ", ".join(user_profile.get("conditions", []))
    allergies = ", ".join(user_profile.get("allergies", []))

    search_query = (
        f"healthier alternative to {product_name} {brand} in Pakistan "
        f"for {conditions} {allergies} "
        f"site:naheed.com OR site:daraz.pk OR site:chaseup.com.pk"
    )

    try:
        tavily_response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": search_query,
                "search_depth": "basic",
                "max_results": 5,
                "include_answer": True
            },
            timeout=15
        )
        tavily_response.raise_for_status()
        tavily_data = tavily_response.json()
        search_answer = tavily_data.get("answer", "")
        search_results = tavily_data.get("results", [])
    except Exception as e:
        print(f"[alternative_finder] Tavily search failed: {e}")
        search_answer = ""
        search_results = []

    synthesis_prompt = f"""Based on these web search results, return ONLY valid JSON with these keys:
{{
  "alternative_product": string or null,
  "alternative_brand": string or null,
  "why_better_roman_urdu": string,
  "where_to_buy": [string],
  "estimated_price_pkr": number or null,
  "online_link": string or null,
  "search_sources": [string]
}}

Search query: {search_query}
Search answer: {search_answer}
Top results:
{json.dumps(search_results[:3], indent=2)}

Rules:
- alternative_product must be a REAL product found in the search results, or null if none found
- why_better_roman_urdu: 1-2 sentences in Roman Urdu (no Urdu script)
- where_to_buy: Pakistani store names from the results
- search_sources: URLs of the results used
- If no real alternative found, return alternative_product=null

Return JSON now."""

    def synthesize_groq():
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model=GROQ_TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You synthesize web search results into JSON. Always return valid JSON only."},
                {"role": "user", "content": synthesis_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=800
        )
        return json.loads(response.choices[0].message.content)

    def synthesize_glm():
        from src.config.settings import GLM_API_KEY, GLM_TEXT_MODEL
        client = OpenAI(
            api_key=GLM_API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4"
        )
        response = client.chat.completions.create(
            model=GLM_TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You synthesize web search results into JSON. Always return valid JSON only."},
                {"role": "user", "content": synthesis_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=800,
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )
        return json.loads(response.choices[0].message.content)

    from src.core.fallback import with_fallback
    result = with_fallback(synthesize_groq, synthesize_glm)
    print(f"[alternative_finder] Synthesis complete alternative: {result.get('alternative_product')}")
    return result
def find_alternative_google_cse(label_data: dict, verdict: dict, user_profile: dict) -> dict:
    """Google Custom Search API + LLM fallback for finding real alternatives."""
    product_name = label_data.get("product_name") or "this product"
    brand = label_data.get("brand") or ""
    conditions = ", ".join(user_profile.get("conditions", []))
    allergies = ", ".join(user_profile.get("allergies", []))

    search_query = (
        f"healthier alternative to {product_name} {brand} in Pakistan "
        f"for {conditions} {allergies} "
        f"site:naheed.com OR site:daraz.pk OR site:chaseup.com.pk"
    )

    if not GOOGLE_CSE_API_KEY or not GOOGLE_CSE_CX:
        raise ValueError("Google CSE API key ya CX configuration missing hai.")

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_CSE_API_KEY,
            "cx": GOOGLE_CSE_CX,
            "q": search_query,
            "num": 5
        }
        response = requests.get(url, params=params, timeout=12)
        response.raise_for_status()
        data = response.json()
        
        search_results = []
        for item in data.get("items", []):
            search_results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "content": item.get("snippet")
            })
    except Exception as e:
        print(f"[alternative_finder] Google Custom Search failed: {e}")
        search_results = []

    synthesis_prompt = f"""Based on these web search results, return ONLY valid JSON with these keys:
{{
  "alternative_product": string or null,
  "alternative_brand": string or null,
  "why_better_roman_urdu": string,
  "where_to_buy": [string],
  "estimated_price_pkr": number or null,
  "online_link": string or null,
  "search_sources": [string]
}}

Search query: {search_query}
Top results:
{json.dumps(search_results[:3], indent=2)}

Rules:
- alternative_product must be a REAL product found in the search results, or null if none found
- why_better_roman_urdu: 1-2 sentences in Roman Urdu (no Urdu script)
- where_to_buy: Pakistani store names from the results
- search_sources: URLs of the results used
- If no real alternative found, return alternative_product=null

Return JSON now."""

    def synthesize_openai():
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_SEARCH_MODEL,
            messages=[
                {"role": "system", "content": "You synthesize web search results into JSON. Always return valid JSON only."},
                {"role": "user", "content": synthesis_prompt}
            ],
            response_format={"type": "json_object"} if "gpt-4o" in OPENAI_SEARCH_MODEL else None,
            temperature=0.3,
            max_tokens=800
        )
        return json.loads(response.choices[0].message.content)

    def synthesize_glm():
        from src.config.settings import GLM_API_KEY, GLM_TEXT_MODEL
        client = OpenAI(
            api_key=GLM_API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4"
        )
        response = client.chat.completions.create(
            model=GLM_TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You synthesize web search results into JSON. Always return valid JSON only."},
                {"role": "user", "content": synthesis_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=800,
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )
        return json.loads(response.choices[0].message.content)

    from src.core.fallback import with_fallback
    result = with_fallback(synthesize_openai, synthesize_glm)
    print(f"[alternative_finder] Google CSE synthesis complete alternative: {result.get('alternative_product')}")
    return result


def find_alternative(label_data, verdict, user_profile):
    from src.core.fallback import with_fallback

    # Chain: OpenAI (Primary) -> Google Custom Search (1st Fallback) -> Tavily (2nd Fallback)
    def google_then_tavily(*args, **kwargs):
        return with_fallback(find_alternative_google_cse, find_alternative_tavily, *args, **kwargs)

    return with_fallback(find_alternative_openai, google_then_tavily, label_data, verdict, user_profile)

