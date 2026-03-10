
def extract_products(page, product_selectors=None, title_selectors=None, limit=5):
    product_selectors = product_selectors or [
        ".s-result-item[data-component-type='s-search-result']",
        ".srp-results .s-item",
        "div[data-id]",
        ".sku-item",
        "[role='listitem']",
    ]
    title_selectors = title_selectors or [
        "h2 a span",
        "h2",
        ".s-item__title",
        "a[title]",
        ".sku-title a",
    ]

    products = []
    for selector in product_selectors:
        products = page.query_selector_all(selector)
        if products:
            break

    results = []
    for product in products:
        title_text = None
        for title_selector in title_selectors:
            try:
                title = product.query_selector(title_selector)
                if title:
                    candidate = (title.inner_text() or "").strip()
                    if candidate:
                        title_text = candidate
                        break
            except Exception:
                continue

        if title_text:
            results.append(title_text)
            if len(results) >= limit:
                break

    return results
