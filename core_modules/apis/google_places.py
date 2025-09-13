import requests
from .base import APIBase
from helpers import normalize_price

class GooglePlacesAPI(APIBase):
    BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    SUPPORTED_CATEGORIES = [
        "museum", "art_gallery", "historical", "monument",
        "restaurant", "cafe", "bar"
    ]

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def supports(self, category: str) -> bool:
        return category in self.SUPPORTED_CATEGORIES

    def search(self, location: str, category: str, budget: float):
        if not self.api_key:
            # Mock response
            return [{
                "name": f"Sample {category.title()} in {location}",
                "lat": 45.4642,
                "lon": 9.19,
                "price": "$$",
                "source": "Google Places (mock)"
            }]

        params = {
            "query": f"{category} in {location}",
            "key": self.api_key,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        if not resp.ok:
            return []

        data = resp.json()
        results = []
        for place in data.get("results", []):
            raw_price = place.get("price_level")
            norm_price = normalize_price(raw_price)
            print("[GooglePlacesAPI] Raw:", raw_price, "-> Norm:", norm_price)
            results.append({
                "name": place.get("name"),
                "lat": place["geometry"]["location"]["lat"],
                "lon": place["geometry"]["location"]["lng"],
                "price": norm_price,
                "rating": place.get("rating", 0),
                "review_count": place.get("user_ratings_total", 0),
                "source": "Google Places"
            })

        return results
