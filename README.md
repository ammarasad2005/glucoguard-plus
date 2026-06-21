# GlucoGuard+ 🛡️

**Apne khaane ka guard banayein. Awaaz mein. Roman Urdu mein.**

A phone-camera app for Pakistan's 33 million diabetics. Snap a photo of any packaged food label, get a personalized verdict in Roman Urdu — spoken aloud for the 40% who can't read.

## The "+" in GlucoGuard+
- **Voice output** — verdict read aloud via gpt-4o-mini-tts
- **Live web search** — actual healthier alternatives available in Pakistan via gpt-4o-search-preview

## Problem
Pakistan has 33M diabetics (world's highest after China). Packaged food labels hide sugars under 50+ chemical names (maltodextrin, dextrose, etc.). 40% of adults can't read the labels at all.

## How it works
1. Photo of food label → gpt-4o-mini reads it (vision)
2. Label + user profile → gpt-4o-mini generates verdict (reasoning)
3. Verdict → gpt-4o-search-preview finds actual healthier alternatives (web search)
4. Verdict → gpt-4o-mini-tts reads it aloud (voice)

## Setup
```bash
pip install -r requirements.txt
# Add your OpenAI key to .env
streamlit run app.py
```

## Tech stack
- Streamlit (UI)
- OpenAI: gpt-4o-mini (vision + reasoning), gpt-4o-search-preview (search), gpt-4o-mini-tts (voice)
- Python 3.11

## Track
Open Innovation — National AI Hackathon, FAST NUCES Islamabad, 16-17 June 2026
