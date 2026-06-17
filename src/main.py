print("GlucoGuard+ — setup check")

from src.config.settings import (
    OPENAI_API_KEY,
    OPENAI_VISION_MODEL,
    OPENAI_TEXT_MODEL,
    OPENAI_SEARCH_MODEL,
    OPENAI_TTS_MODEL,
)

key_preview = OPENAI_API_KEY[:12] + "..." if OPENAI_API_KEY else "None"
print(f"Key preview: {key_preview}")
print(f"Vision model: {OPENAI_VISION_MODEL}")
print(f"Text model: {OPENAI_TEXT_MODEL}")
print(f"Search model: {OPENAI_SEARCH_MODEL}")
print(f"TTS model: {OPENAI_TTS_MODEL}")

print("Setup theek hai. Agla step try karein.")
