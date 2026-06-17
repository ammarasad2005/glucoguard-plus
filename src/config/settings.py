import os
from dotenv import load_dotenv

# Call load_dotenv() at module import time
load_dotenv()

# Define environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
OPENAI_SEARCH_MODEL = os.getenv("OPENAI_SEARCH_MODEL", "gpt-4o-search-preview")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "nova")

def validate_env():
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY nahi mila. Hackathon organizers se shared key lein aur .env mein daalein.")

# Call validate_env() at the bottom of the file
validate_env()

# Fallback provider keys (optional — fallback only triggers if OpenAI fails)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_VISION_MODEL = os.getenv("GEMINI_VISION_MODEL", "gemini-2.0-flash")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_TEXT_MODEL = os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-AriaNeural")
FALLBACK_ENABLED = os.getenv("FALLBACK_ENABLED", "false").lower() == "true"

def fallback_status() -> dict:
    """Return a dict showing which fallback providers are configured."""
    return {
        "gemini": bool(GEMINI_API_KEY and GEMINI_API_KEY.startswith("AIza")),
        "groq": bool(GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_")),
        "tavily": bool(TAVILY_API_KEY and TAVILY_API_KEY.startswith("tvly-")),
        "edge_tts": True,  # always available, no key needed
    }
