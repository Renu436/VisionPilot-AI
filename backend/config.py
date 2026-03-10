
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
DEFAULT_SITE = os.getenv("DEFAULT_SITE", "amazon_in")
TARGET_SITES = [
    site.strip()
    for site in os.getenv("TARGET_SITES", "amazon_in,flipkart,ebay,walmart,bestbuy").split(",")
    if site.strip()
]
