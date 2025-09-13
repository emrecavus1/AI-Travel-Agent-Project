import requests
from .base import APIBase
from helpers import normalize_price

class YelpAPI(APIBase):
    BASE_URL = "https://api.yelp.com/v3/businesses/search"
    SUPPORTED_CATEGORIES = [
        "restaurant", "cafe", "bar", "winery", "club", "pub"
    ]

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def supports(self, category: str) -> bool:
        return category in self.SUPPORTED_CATEGORIES

    def search(self, location: str, category: str, budget: float):
        if not self.api_key:
            return [{
                "name": f"Mock {category.title()} in {location}",
                "lat": 40.7128,
                "lon": -74.0060,
                "price": "$",
                "source": "Yelp (mock)"
            }]

        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "location": location,
            "term": category,
            "limit": 5
        }

        resp = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
        if not resp.ok:
            return []

        data = resp.json()
        results = []
        for b in data.get("businesses", []):
            raw_price = b.get("price")
            norm_price = normalize_price(raw_price)
            print("[GooglePlacesAPI] Raw:", raw_price, "-> Norm:", norm_price)
            results.append({
                "name": b.get("name"),
                "lat": b["coordinates"]["latitude"],
                "lon": b["coordinates"]["longitude"],
                "price": norm_price,
                "rating": b.get("rating", 0),
                "review_count": b.get("review_count", 0),
                "source": "Yelp"
            })

        return results
