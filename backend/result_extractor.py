
def extract_products(page):

    products = page.query_selector_all(".s-result-item")

    results = []

    for product in products[:5]:
        title = product.query_selector("h2")
        if title:
            results.append(title.inner_text())

    return results
