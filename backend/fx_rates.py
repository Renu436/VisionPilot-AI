import time
from typing import Dict

import requests


_CACHE = {
    "expires_at": 0.0,
    "rates": None,
}


def _fetch_inr_rate(base_currency: str, api_url_template: str, timeout_seconds: float = 4.0):
    url = api_url_template.format(base=base_currency, symbols="INR")
    response = requests.get(url, timeout=timeout_seconds)
    response.raise_for_status()
    payload = response.json()
    rates = payload.get("rates") or {}
    inr_rate = rates.get("INR")
    if inr_rate is None:
        raise ValueError(f"Missing INR rate for base {base_currency}")
    return float(inr_rate)


def get_currency_to_inr_rates(
    *,
    fallback_rates: Dict[str, float],
    api_url_template: str,
    refresh_seconds: int,
):
    now = time.time()
    cached = _CACHE.get("rates")
    if cached and now < float(_CACHE.get("expires_at", 0.0)):
        return cached

    rates = {
        "INR": 1.0,
        "USD": float(fallback_rates.get("USD", 83.0)),
        "EUR": float(fallback_rates.get("EUR", 90.0)),
        "GBP": float(fallback_rates.get("GBP", 105.0)),
        "source": "fallback",
    }

    live_ok = True
    for currency in ("USD", "EUR", "GBP"):
        try:
            rates[currency] = _fetch_inr_rate(currency, api_url_template)
        except Exception:
            live_ok = False

    rates["source"] = "live+fallback" if not live_ok else "live"
    _CACHE["rates"] = rates
    _CACHE["expires_at"] = now + max(int(refresh_seconds), 60)
    return rates
