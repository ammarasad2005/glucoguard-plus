from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE, EDGE_TTS_VOICE

def init_client():
    return OpenAI(api_key=OPENAI_API_KEY)

def build_speech_text(verdict: dict, alternative: dict = None) -> str:
    """Build a natural Roman Urdu speech string from the verdict + alternative."""
    parts = []

    verdict_text = verdict.get("verdict_reason_roman_urdu", "")
    if verdict_text:
        parts.append(verdict_text)

    sugars = verdict.get("hidden_sugars_detected", [])
    if sugars:
        sugar_names = [s.get("name", "") for s in sugars[:3]]
        parts.append(f"Is mein {len(sugars)} chhupi hui cheeniyan hain: {', '.join(sugar_names)}.")

    nutrition = verdict.get("nutrition_analysis", {})
    sugar_g = nutrition.get("sugar_g_per_serving")
    sugar_pct = nutrition.get("sugar_pct_of_daily_limit")
    if sugar_g is not None and sugar_pct is not None:
        parts.append(f"Ek serving mein {sugar_g} gram cheeni hai, jo aap ki daily limit ka {int(sugar_pct)} percent hai.")

    if alternative and alternative.get("alternative_product"):
        alt_name = alternative["alternative_product"]
        alt_brand = alternative.get("alternative_brand", "")
        alt_why = alternative.get("why_better_roman_urdu", "")
        price = alternative.get("estimated_price_pkr")
        store = ", ".join(alternative.get("where_to_buy", [])[:2])

        alt_text = f"Behtar alternative: {alt_name}"
        if alt_brand:
            alt_text += f" by {alt_brand}"
        if price:
            alt_text += f", keemat taqreeban {price} rupee"
        if store:
            alt_text += f", {store} par milta hai"
        alt_text += f". {alt_why}"
        parts.append(alt_text)

    teachable = verdict.get("teachable_moment_roman_urdu", "")
    if teachable:
        parts.append(teachable)

    return " ".join(parts)

def generate_voice_openai(text: str) -> bytes:
    """Generate an MP3 audio of the given text using OpenAI TTS. Returns MP3 bytes."""
    if not text or not text.strip():
        raise ValueError("Speech text khali hai. Kuch sunane ke liye nahi mila.")

    client = init_client()

    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,  # "nova" by default — female, natural
        input=text,
        response_format="mp3"
    )

    # response.content gives the raw MP3 bytes
    audio_bytes = response.content
    print(f"[voice_output] Voice generated — {len(audio_bytes)} bytes, text length {len(text)}")
    return audio_bytes

def generate_voice_edge_tts(text: str) -> bytes:
    """edge-tts fallback. No API key needed. Uses Microsoft Edge neural voices."""
    import asyncio
    import edge_tts
    from io import BytesIO

    async def _generate():
        communicate = edge_tts.Communicate(text, EDGE_TTS_VOICE)
        audio_buffer = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        return audio_buffer.getvalue()

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import threading
            result = [None]
            def run():
                new_loop = asyncio.new_event_loop()
                result[0] = new_loop.run_until_complete(_generate())
                new_loop.close()
            t = threading.Thread(target=run)
            t.start()
            t.join()
            audio_bytes = result[0]
        else:
            audio_bytes = loop.run_until_complete(_generate())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(_generate())

    print(f"[voice_output] edge-tts fallback generated — {len(audio_bytes)} bytes")
    return audio_bytes

def generate_voice(text):
    from src.core.fallback import with_fallback
    return with_fallback(generate_voice_openai, generate_voice_edge_tts, text)
