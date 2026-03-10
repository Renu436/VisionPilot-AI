
from google import genai
from PIL import Image
import json
try:
    from .config import GEMINI_API_KEY, GEMINI_MODEL
except ImportError:
    from config import GEMINI_API_KEY, GEMINI_MODEL

client = None

SYSTEM_PROMPT = '''
You are an AI web navigation agent.

User goal: {goal}

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

def analyze_screen(goal, screenshot_path):
    if not GEMINI_API_KEY:
        return {"action": "done", "text": "Missing GEMINI_API_KEY in environment"}

    global client
    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        img = Image.open(screenshot_path)
    except Exception:
        return {"action": "scroll"}

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            SYSTEM_PROMPT.format(goal=goal),
            img
        ]
    )

    try:
        text = (response.text or "").strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if len(lines) >= 3:
                text = "\n".join(lines[1:-1]).strip()
        return json.loads(text)
    except Exception:
        return {"action":"scroll"}
