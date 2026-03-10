
try:
    from .result_extractor import extract_products
except ImportError:
    from result_extractor import extract_products

def execute_action(browser, action, site_profile=None):
    if not isinstance(action, dict):
        return False

    site_profile = site_profile or {}
    search_selectors = site_profile.get("search_input_selectors")
    product_selectors = site_profile.get("product_selectors")
    title_selectors = site_profile.get("title_selectors")

    name = action.get("action")

    if name == "click_search":
        browser.click_search(search_selectors)

    elif name == "type_search":
        browser.type_search(action.get("text",""), search_selectors)

    elif name == "scroll":
        browser.scroll()

    elif name == "extract_results":
        results = extract_products(
            browser.page,
            product_selectors=product_selectors,
            title_selectors=title_selectors,
        )
        print("Top Results:", results)
        return len(results) > 0

    elif name == "done":
        return True

    return False
