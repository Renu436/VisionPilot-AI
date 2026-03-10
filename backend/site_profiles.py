SITE_PROFILES = {
    "amazon_in": {
        "name": "Amazon India",
        "url": "https://www.amazon.in",
        "search_input_selectors": ["#twotabsearchtextbox", "input[name='field-keywords']"],
        "product_selectors": [".s-result-item[data-component-type='s-search-result']"],
        "title_selectors": ["h2 a span", "h2 span"],
    },
    "amazon_com": {
        "name": "Amazon US",
        "url": "https://www.amazon.com",
        "search_input_selectors": ["#twotabsearchtextbox", "input[name='field-keywords']"],
        "product_selectors": [".s-result-item[data-component-type='s-search-result']"],
        "title_selectors": ["h2 a span", "h2 span"],
    },
    "flipkart": {
        "name": "Flipkart",
        "url": "https://www.flipkart.com",
        "search_input_selectors": ["input[name='q']", "input[title='Search for products, brands and more']"],
        "product_selectors": ["div[data-id]", "div._75nlfW"],
        "title_selectors": ["a[title]", "div.KzDlHZ", "a.wjcEIp"],
    },
    "ebay": {
        "name": "eBay",
        "url": "https://www.ebay.com",
        "search_input_selectors": ["#gh-ac", "input[type='text'][name='_nkw']"],
        "product_selectors": [".srp-results .s-item"],
        "title_selectors": [".s-item__title"],
    },
    "walmart": {
        "name": "Walmart",
        "url": "https://www.walmart.com",
        "search_input_selectors": ["input[aria-label='Search']", "input[type='search']"],
        "product_selectors": ["[data-item-id]", "[data-testid='list-view'] [role='listitem']"],
        "title_selectors": ["[data-automation-id='product-title']", "a span"],
    },
    "bestbuy": {
        "name": "Best Buy",
        "url": "https://www.bestbuy.com",
        "search_input_selectors": ["#gh-search-input", "input[type='search']"],
        "product_selectors": [".sku-item"],
        "title_selectors": [".sku-title a", "h4 a"],
    },
}

SITE_ALIASES = {
    "amazon": "amazon_in",
    "amazon.in": "amazon_in",
    "amazon.com": "amazon_com",
    "flipkart": "flipkart",
    "ebay": "ebay",
    "walmart": "walmart",
    "bestbuy": "bestbuy",
    "best buy": "bestbuy",
}
