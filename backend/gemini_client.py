import warnings

warnings.filterwarnings(
    "ignore",
    message=".*Python version 3\\.9 past its end of life.*",
    category=FutureWarning,
)
warnings.filterwarnings(
    "ignore",
    message=".*urllib3 v2 only supports OpenSSL 1\\.1\\.1\\+.*",
)

from google import genai
from PIL import Image
import json
import re
try:
    from .config import GEMINI_API_KEY, GEMINI_MODEL
except ImportError:
    from config import GEMINI_API_KEY, GEMINI_MODEL

client = None

SYSTEM_PROMPT = '''
You are an AI web navigation agent.

User goal: {goal}
Target shopping site: {site_name}

You receive a screenshot of a webpage.
Understand the UI and decide the next step.

Allowed actions:
click_search
type_search
scroll
extract_results
done

Return JSON only.

Example:
{
 "action":"type_search",
 "text":"laptop under 50000"
}
'''


VALID_ACTIONS = {"click_search", "type_search", "scroll", "extract_results", "done"}


def _extract_json_object(text):
    value = (text or "").strip()
    if not value:
        return None

    if value.startswith("```"):
        lines = value.splitlines()
        if len(lines) >= 3:
            value = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(value)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    # Fallback: extract first JSON-like object from verbose model output.
    match = re.search(r"\{[\s\S]*\}", value)
    if not match:
        return None

    try:
        parsed = json.loads(match.group(0))
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return None
    return None


def _normalize_action(parsed):
    if not isinstance(parsed, dict):
        return {"action": "scroll"}

    action = str(parsed.get("action", "")).strip().lower()
    synonyms = {
        "search": "type_search",
        "enter_search": "type_search",
        "clicksearch": "click_search",
        "extract": "extract_results",
        "finish": "done",
    }
    action = synonyms.get(action, action)

    if action not in VALID_ACTIONS:
        action = "scroll"

    result = {"action": action}
    if action == "type_search":
        result["text"] = str(parsed.get("text", "")).strip()
    return result


def analyze_screen(goal, screenshot_path, site_name=""):
    if not GEMINI_API_KEY:
        return {"action": "done", "text": "Missing GEMINI_API_KEY in environment"}

    global client
    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        img = Image.open(screenshot_path)
    except Exception:
        return {"action": "scroll"}

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                SYSTEM_PROMPT.format(goal=goal, site_name=site_name or "unspecified"),
                img
            ]
        )
    except Exception:
        return {"action": "scroll"}

    try:
        parsed = _extract_json_object(getattr(response, "text", "") or "")
        if not parsed:
            return {"action": "extract_results"}
        return _normalize_action(parsed)
    except Exception:
        return {"action": "extract_results"}
