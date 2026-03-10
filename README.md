
# VisionPilot AI – Multi-Site Shopping Agent

AI agent that uses Gemini Vision + Playwright to navigate shopping sites and extract product results.

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

The agent auto-detects site intent from your goal (for example: `on flipkart`), scans all configured sites, and ranks combined results using normalized INR price.

## Optional Environment Variables

- `DEFAULT_SITE=amazon_in`
- `TARGET_SITES=amazon_in,amazon_com,flipkart,ebay,walmart,bestbuy`
- `USD_TO_INR=83.0`
- `EUR_TO_INR=90.0`
- `GBP_TO_INR=105.0`
- `FX_API_URL_TEMPLATE=https://api.exchangerate.host/latest?base={base}&symbols={symbols}`
- `FX_REFRESH_SECONDS=21600` (6-hour FX cache)

## Demo Prompts

Search laptop under 50000
Search gaming mouse on ebay
Find 4k monitor on best buy
