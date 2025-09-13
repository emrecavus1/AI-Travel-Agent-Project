import requests
from datetime import timedelta


def derived_inputs(start_date, days, budget):
    daily_budget = budget / max(days, 1)
    end_date = start_date + timedelta(days - 1)
    return daily_budget, end_date


def normalize_price(raw_price):
    """
    Normalize Google Places / Yelp price levels into an estimated numeric value.
    - Google: price_level is int 0–4
    - Yelp: price is string "$"/"€" repeated 1–4 times
    - N/A or missing -> 0
    """

    if raw_price is None:
        return 0

    # Handle Google int or stringified int
    try:
        if isinstance(raw_price, (int, float)) or str(raw_price).isdigit():
            raw_price = int(raw_price)
            mapping = {0: 0, 1: 15, 2: 35, 3: 75, 4: 120}
            return mapping.get(raw_price, 0)
    except Exception:
        pass

    # Handle Yelp strings ($ or €)
    if isinstance(raw_price, str):
        raw_price = raw_price.strip()
        # Normalize € to $
        raw_price = raw_price.replace("€", "$")
        mapping = {"$": 15, "$$": 35, "$$$": 75, "$$$$": 120}
        return mapping.get(raw_price, 0)

    return 0


