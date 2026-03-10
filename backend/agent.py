
try:
    from .browser_controller import BrowserController
    from .gemini_client import analyze_screen
    from .action_executor import execute_action
    from .config import DEFAULT_SITE, TARGET_SITES
    from .site_profiles import SITE_PROFILES, SITE_ALIASES
except ImportError:
    from browser_controller import BrowserController
    from gemini_client import analyze_screen
    from action_executor import execute_action
    from config import DEFAULT_SITE, TARGET_SITES
    from site_profiles import SITE_PROFILES, SITE_ALIASES

class VisionPilotAgent:

    def __init__(self, browser=None):
        self.browser = browser or BrowserController()

    def _site_ids_from_goal(self, goal):
        normalized = (goal or "").lower()
        chosen = []
        for alias, site_id in SITE_ALIASES.items():
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

        self.browser.open_site(site_profile["url"])

        if normalized_goal:
            self.browser.click_search(search_selectors)
            self.browser.type_search(normalized_goal, search_selectors)

        for step in range(10):
            screenshot = self.browser.screenshot()
            action = analyze_screen(goal, screenshot, site_name=site_profile.get("name", ""))

            if not isinstance(action, dict) or "action" not in action:
                action = {"action": "scroll"}

            action_name = action.get("action", "scroll")
            repeated_actions[action_name] = repeated_actions.get(action_name, 0) + 1

            if action_name in {"scroll", "click_search"} and repeated_actions[action_name] >= 3:
                action = {"action": "extract_results"}
                action_name = "extract_results"

            print(f"[{site_profile.get('name', 'Site')}] Agent Decision:", action)
            finished = execute_action(self.browser, action, site_profile=site_profile)

            if finished:
                return True

            if action_name == "scroll" and step == 4 and normalized_goal:
                self.browser.click_search(search_selectors)
                self.browser.type_search(normalized_goal, search_selectors)

        return False

    def run(self, goal):
        site_ids = self._site_ids_from_goal(goal)

        for site_id in site_ids:
            site_profile = SITE_PROFILES.get(site_id)
            if not site_profile:
                continue

            if self._run_on_site(goal, site_profile):
                return f"Task Completed on {site_profile.get('name', site_id)}"

        site_names = [SITE_PROFILES[s]["name"] for s in site_ids if s in SITE_PROFILES]
        return f"Stopped after max steps (no actionable results found) across: {', '.join(site_names)}"
