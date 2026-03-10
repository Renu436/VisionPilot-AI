
try:
    from .result_extractor import extract_products
except ImportError:
    from result_extractor import extract_products

def execute_action(browser, action):

    name = action.get("action")

    if name == "click_search":
        browser.click_search()

    elif name == "type_search":
        browser.type_search(action.get("text",""))

    elif name == "scroll":
        browser.scroll()

    elif name == "extract_results":
        results = extract_products(browser.page)
        print("Top Results:", results)

    elif name == "done":
        return True

    return False
