
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
DEFAULT_SITE = os.getenv("DEFAULT_SITE", "amazon_in").strip().lower()
TARGET_SITES = [
    site.strip().lower()
    for site in os.getenv(
        "TARGET_SITES",
        "amazon_in,amazon_com,flipkart,ebay,walmart,bestbuy",
    ).split(",")
    if site.strip()
]

# Currency normalization (used for cross-site ranking).
USD_TO_INR = float(os.getenv("USD_TO_INR", "83.0"))
EUR_TO_INR = float(os.getenv("EUR_TO_INR", "90.0"))
GBP_TO_INR = float(os.getenv("GBP_TO_INR", "105.0"))
FX_API_URL_TEMPLATE = os.getenv(
    "FX_API_URL_TEMPLATE",
    "https://api.exchangerate.host/latest?base={base}&symbols={symbols}",
).strip()
FX_REFRESH_SECONDS = int(os.getenv("FX_REFRESH_SECONDS", "21600"))
