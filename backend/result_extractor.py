
from urllib.parse import urljoin


def extract_products(
    page,
    product_selectors=None,
    title_selectors=None,
    link_selectors=None,
    price_selectors=None,
    limit=5,
):
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
    link_selectors = link_selectors or [
        "h2 a",
        "a.a-link-normal.s-no-outline",
        "a.a-link-normal",
    ]
    price_selectors = price_selectors or [
        ".a-price .a-offscreen",
        ".a-price-whole",
        "[data-testid='price-wrap']",
    ]

    products = []
    for selector in product_selectors:
        products = page.query_selector_all(selector)
        if products:
            break

    results = []
    seen_titles = set()
    current_url = page.url or ""

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

        if not title_text:
            continue

        normalized = title_text.lower()
        if normalized in seen_titles:
            continue
        seen_titles.add(normalized)

        product_url = None
        for link_selector in link_selectors:
            try:
                link = product.query_selector(link_selector)
                if not link:
                    continue
                href = (link.get_attribute("href") or "").strip()
                if href:
                    product_url = urljoin(current_url, href)
                    break
            except Exception:
                continue

        product_price = None
        for price_selector in price_selectors:
            try:
                price = product.query_selector(price_selector)
                if not price:
                    continue
                candidate = (price.inner_text() or "").strip()
                if candidate:
                    product_price = candidate
                    break
            except Exception:
                continue

        results.append(
            {
                "title": title_text,
                "price": product_price or "N/A",
                "url": product_url or "",
            }
        )
        if len(results) >= limit:
            break

    return results
