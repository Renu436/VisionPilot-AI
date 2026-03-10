
import re
from urllib.parse import quote_plus

try:
    from .browser_controller import BrowserController
    from .gemini_client import analyze_screen
    from .action_executor import execute_action
    from .config import (
        DEFAULT_SITE,
        TARGET_SITES,
        USD_TO_INR,
        EUR_TO_INR,
        GBP_TO_INR,
        FX_API_URL_TEMPLATE,
        FX_REFRESH_SECONDS,
    )
    from .fx_rates import get_currency_to_inr_rates
    from .site_profiles import SITE_PROFILES, SITE_ALIASES
except ImportError:
    from browser_controller import BrowserController
    from gemini_client import analyze_screen
    from action_executor import execute_action
    from config import (
        DEFAULT_SITE,
        TARGET_SITES,
        USD_TO_INR,
        EUR_TO_INR,
        GBP_TO_INR,
        FX_API_URL_TEMPLATE,
        FX_REFRESH_SECONDS,
    )
    from fx_rates import get_currency_to_inr_rates
    from site_profiles import SITE_PROFILES, SITE_ALIASES

class VisionPilotAgent:

    def __init__(self, browser=None):
        self.browser = browser or BrowserController()

    def close(self):
        """Release browser resources for this agent instance."""
        try:
            self.browser.close()
        except Exception:
            pass

    def _site_ids_from_goal(self, goal):
        normalized = (goal or "").lower()
        chosen = []

        # Match more specific aliases first (e.g. "amazon.com" before "amazon").
        sorted_aliases = sorted(SITE_ALIASES.items(), key=lambda item: len(item[0]), reverse=True)
        for alias, site_id in sorted_aliases:
            if alias in normalized and site_id in SITE_PROFILES and site_id not in chosen:
                chosen.append(site_id)

        for site_id in TARGET_SITES:
            if site_id in SITE_PROFILES and site_id not in chosen:
                chosen.append(site_id)

        if not chosen:
            chosen = [DEFAULT_SITE] if DEFAULT_SITE in SITE_PROFILES else ["amazon_in"]

        return chosen

    def _run_on_site(self, goal, site_profile):
        normalized_goal = (goal or "").strip()
        repeated_actions = {}
        search_selectors = site_profile.get("search_input_selectors")
        site_name = site_profile.get("name", "Site")
        collected_results = []

        try:
            self.browser.open_site(site_profile["url"])
        except Exception as exc:
            raise RuntimeError(f"[{site_name}] Failed to open site: {exc}") from exc

        if normalized_goal:
            self.browser.click_search(search_selectors)
            typed = self.browser.type_search(normalized_goal, search_selectors)
            if not typed:
                # Fallback path for sites with dynamic overlays/banners blocking input interaction.
                search_url_template = site_profile.get("search_url_template")
                if search_url_template:
                    direct_url = search_url_template.format(query=quote_plus(normalized_goal))
                    self.browser.open_site(direct_url)

        for step in range(10):
            try:
                screenshot = self.browser.screenshot()
            except Exception as exc:
                raise RuntimeError(f"[{site_name}] Failed to capture screenshot: {exc}") from exc

            action = analyze_screen(goal, screenshot, site_name=site_profile.get("name", ""))

            if not isinstance(action, dict) or "action" not in action:
                action = {"action": "scroll"}

            action_name = action.get("action", "scroll")
            repeated_actions[action_name] = repeated_actions.get(action_name, 0) + 1

            if action_name in {"scroll", "click_search"} and repeated_actions[action_name] >= 3:
                action = {"action": "extract_results"}
                action_name = "extract_results"

            print(f"[{site_name}] Agent Decision:", action)
            try:
                action_result = execute_action(self.browser, action, site_profile=site_profile)
            except Exception as exc:
                raise RuntimeError(f"[{site_name}] Action execution failed: {exc}") from exc

            finished = bool(action_result.get("finished"))
            step_results = action_result.get("results") or []
            if step_results:
                collected_results = step_results

            # If model says "done" before extraction, do one last scrape attempt.
            if action_name == "done" and not collected_results:
                fallback = execute_action(
                    self.browser,
                    {"action": "extract_results"},
                    site_profile=site_profile,
                )
                fallback_results = fallback.get("results") or []
                # Only treat "done" as terminal if extraction actually produced results.
                if fallback_results:
                    collected_results = fallback_results
                finished = bool(fallback_results)

            if finished:
                return {"completed": True, "results": collected_results}

            if action_name == "scroll" and step == 4 and normalized_goal:
                self.browser.click_search(search_selectors)
                typed = self.browser.type_search(normalized_goal, search_selectors)
                if not typed:
                    search_url_template = site_profile.get("search_url_template")
                    if search_url_template:
                        direct_url = search_url_template.format(query=quote_plus(normalized_goal))
                        self.browser.open_site(direct_url)

        return {"completed": False, "results": collected_results}

    def _parse_price_value(self, price_text):
        if not price_text:
            return None
        cleaned = str(price_text).replace(",", "")
        match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
        if not match:
            return None
        try:
            return float(match.group(1))
        except ValueError:
            return None

    def _detect_currency(self, price_text, site_name):
        text = (price_text or "").lower()
        site = (site_name or "").lower()

        if any(token in text for token in ["₹", "rs", "inr"]):
            return "INR"
        if any(token in text for token in ["$", "usd"]):
            return "USD"
        if any(token in text for token in ["€", "eur"]):
            return "EUR"
        if any(token in text for token in ["£", "gbp"]):
            return "GBP"

        if "india" in site or "flipkart" in site:
            return "INR"
        if "us" in site or "ebay" in site or "walmart" in site or "best buy" in site:
            return "USD"
        return None

    def _normalize_to_inr(self, amount, currency):
        if amount is None or currency is None:
            return None
        if currency == "INR":
            return amount
        if currency in self.currency_to_inr:
            return amount * float(self.currency_to_inr[currency])
        return None

    def run(self, goal):
        self.currency_to_inr = get_currency_to_inr_rates(
            fallback_rates={
                "USD": USD_TO_INR,
                "EUR": EUR_TO_INR,
                "GBP": GBP_TO_INR,
            },
            api_url_template=FX_API_URL_TEMPLATE,
            refresh_seconds=FX_REFRESH_SECONDS,
        )

        site_ids = self._site_ids_from_goal(goal)
        all_results = []
        site_errors = []
        visited_sites = []

        for site_id in site_ids:
            site_profile = SITE_PROFILES.get(site_id)
            if not site_profile:
                continue

            site_name = site_profile.get("name", site_id)
            visited_sites.append(site_name)

            try:
                run_result = self._run_on_site(goal, site_profile)
            except RuntimeError as exc:
                site_errors.append(str(exc))
                continue

            site_results = run_result.get("results") or []
            for item in site_results:
                if isinstance(item, dict):
                    item_with_site = dict(item)
                    item_with_site["site"] = site_name
                    raw_price_value = self._parse_price_value(item_with_site.get("price"))
                    currency = self._detect_currency(item_with_site.get("price"), site_name)
                    normalized_inr = self._normalize_to_inr(raw_price_value, currency)
                    item_with_site["currency"] = currency or "UNKNOWN"
                    item_with_site["normalized_price_inr"] = (
                        round(normalized_inr, 2) if normalized_inr is not None else None
                    )
                    item_with_site["_sort_price_inr"] = (
                        normalized_inr if normalized_inr is not None else float("inf")
                    )
                    all_results.append(item_with_site)

        ranked_results = sorted(
            all_results,
            key=lambda item: (
                item.get("_sort_price_inr") == float("inf"),
                item.get("_sort_price_inr"),
            ),
        )

        # Remove internal scoring field before returning API response.
        for item in ranked_results:
            item.pop("_sort_price_inr", None)

        best_result = ranked_results[0] if ranked_results else None

        if ranked_results:
            return {
                "status": "success",
                "site": ", ".join(visited_sites),
                "message": f"Scanned {len(visited_sites)} sites and ranked {len(ranked_results)} results.",
                "results": ranked_results,
                "optimal_result": best_result,
                "fx_source": self.currency_to_inr.get("source", "fallback"),
            }

        if site_errors:
            return {
                "status": "error",
                "site": ", ".join(visited_sites) if visited_sites else "N/A",
                "message": " | ".join(site_errors),
                "results": [],
            }

        return {
            "status": "partial",
            "site": ", ".join(visited_sites) if visited_sites else "N/A",
            "message": "No clear product results extracted after scanning configured sites.",
            "results": [],
        }
