"""Shared Gemini helpers, used by the fact-checker (Step 3) and the agent (Step 4)."""
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MAIN_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
LITE_MODEL = os.getenv("GEMINI_LITE_MODEL", "gemini-3.5-flash-lite")

# Free-tier limits are per minute, so retry automatically on 429 "too many requests"
# and on temporary server errors, waiting a little longer each time.
client = genai.Client(
    http_options=types.HttpOptions(
        timeout=90_000,  # milliseconds
        retry_options=types.HttpRetryOptions(attempts=5, initial_delay=2.0, max_delay=30.0),
    )
)


def generate_json(prompt: str, model: str = LITE_MODEL) -> dict:
    """Ask the model for a JSON object and return it as a Python dict."""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    text = (response.text or "").strip()
    if text.startswith("```"):  # strip markdown fences if the model adds them anyway
        text = text.strip("`").removeprefix("json").strip()
    return json.loads(text)
