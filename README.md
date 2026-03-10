
# VisionPilot AI – Multi-Site Shopping Agent

AI agent that uses Gemini Vision + Playwright to navigate shopping sites.

## Setup

1. Install Python 3.10+

2. Install dependencies

pip install -r requirements.txt

3. Install browser automation

playwright install chromium

4. Add Gemini API Key

Copy `.env.example` to `.env`

Paste your Gemini key:

GEMINI_API_KEY=YOUR_KEY

5. Run backend

uvicorn backend.main:app --reload

6. Run frontend

streamlit run frontend/app.py

## Supported Shopping Sites

- Amazon India
- Amazon US
- Flipkart
- eBay
- Walmart
- Best Buy

The agent auto-detects site intent from your goal (for example: `on flipkart`) and can also try multiple sites from environment configuration.

## Optional Environment Variables

- `DEFAULT_SITE=amazon_in`
- `TARGET_SITES=amazon_in,flipkart,ebay,walmart,bestbuy`

## Demo Prompts

Search laptop under 50000
Search gaming mouse on ebay
Find 4k monitor on best buy
