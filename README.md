
# VisionPilot AI – Hackathon Ready Project

AI agent that uses Gemini Vision + Playwright to navigate websites.

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

## Demo Prompt

Search laptop under 50000
