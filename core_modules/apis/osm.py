import requests
from .base import APIBase

class OSMAPI(APIBase):
    BASE_URL = "https://overpass-api.de/api/interpreter"
    SUPPORTED_CATEGORIES = [
        "park", "garden", "lake", "beach", "mountain", "market", "store"
    ]

    def supports(self, category: str) -> bool:
        return category in self.SUPPORTED_CATEGORIES

    def search(self, location: str, category: str, budget: float):
        # For now, mock (real implementation would use geocoding + Overpass QL)
        return [{
            "name": f"Mock {category.title()} near {location}",
            "lat": 48.1351,
            "lon": 11.5820,
            "price": 0,
            "source": "OpenStreetMap (mock)"
        }]
