import os
from dotenv import load_dotenv
import streamlit as st

# Call load_dotenv() at module import time
load_dotenv()

# Define a helper to load secrets from Streamlit secrets or environment variables
def get_secret(key, default=None):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

# Define environment variables
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
OPENAI_VISION_MODEL = get_secret("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_TEXT_MODEL = get_secret("OPENAI_TEXT_MODEL", "gpt-4o-mini")
OPENAI_SEARCH_MODEL = get_secret("OPENAI_SEARCH_MODEL", "gpt-4o-search-preview")
OPENAI_TTS_MODEL = get_secret("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TTS_VOICE = get_secret("OPENAI_TTS_VOICE", "nova")

def validate_env():
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY nahi mila. Hackathon organizers se shared key lein aur secrets mein daalein.")

# Call validate_env() at the bottom of the file
validate_env()

# Fallback provider keys (optional — fallback only triggers if OpenAI fails)
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
GEMINI_VISION_MODEL = get_secret("GEMINI_VISION_MODEL", "gemini-2.0-flash")
GROQ_API_KEY = get_secret("GROQ_API_KEY")
GROQ_TEXT_MODEL = get_secret("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")
EDGE_TTS_VOICE = get_secret("EDGE_TTS_VOICE", "en-US-AriaNeural")
FALLBACK_ENABLED = str(get_secret("FALLBACK_ENABLED", "false")).lower() == "true"

# GLM Fallback keys (Zhipu AI)
GLM_API_KEY = get_secret("GLM_API_KEY")
GLM_TEXT_MODEL = get_secret("GLM_TEXT_MODEL", "GLM-4.7-Flash")
GLM_VISION_MODEL = get_secret("GLM_VISION_MODEL", "GLM-4.6V-Flash")


def fallback_status() -> dict:
    """Return a dict showing which fallback providers are configured."""
    return {
        "gemini": bool(GEMINI_API_KEY and GEMINI_API_KEY.startswith("AIza")),
        "groq": bool(GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_")),
        "tavily": bool(TAVILY_API_KEY and TAVILY_API_KEY.startswith("tvly-")),
        "glm": bool(GLM_API_KEY),
        "edge_tts": True,  # always available, no key needed
    }
