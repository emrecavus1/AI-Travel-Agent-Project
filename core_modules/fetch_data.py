from .mappings import PREFERENCE_MAP
from .apis.google_places import GooglePlacesAPI
from .apis.yelp import YelpAPI
from .apis.osm import OSMAPI
from dotenv import load_dotenv
from sklearn.cluster import KMeans
import os
import numpy as np


load_dotenv()
google_key = os.getenv("GOOGLE_PLACES_API")
yelp_key = os.getenv("YELP_API")
print("Google Key Loaded:", bool(google_key))
print("Yelp Key Loaded:", bool(yelp_key))


class APIFilter:
    def __init__(self, preferences, daily_budget, location, start_date, end_date, days):
        self.preferences = [p.lower() for p in preferences]
        self.daily_budget = daily_budget
        self.location = location
        self.start_date = start_date
        self.days = days
        self.end_date = end_date
        self.apis = [
            GooglePlacesAPI(api_key=google_key),
            YelpAPI(api_key=yelp_key),
            OSMAPI()
        ]

    def get_allowed_categories(self):
            allowed = []
            for pref in self.preferences:
                pref_data = PREFERENCE_MAP.get(pref, {})
                if pref_data:
                    api_name = pref_data.get("api")
                    categories = pref_data.get("categories", [])
                    for cat in categories:
                        allowed.append({"api": api_name, "category": cat})
            return allowed
    
    def query(self):
        results = []
        for api in self.apis:
            for category in self.get_allowed_categories():
                if api.supports(category["category"]):
                    api_results = api.search(self.location, category["category"], self.daily_budget)
                    results.extend(api_results)
        return results


    @staticmethod
    def get_coordinates(results):
        coords, indexes = [], []
        for i, r in enumerate(results):
            # Some APIs might use 'lat'/'lon', others 'latitude'/'longitude'
            lat = r.get("lat") or r.get("latitude")
            lon = r.get("lon") or r.get("longitude")

            try:
                lat = float(lat)
                lon = float(lon)
            except (TypeError, ValueError):
                continue  # skip if invalid

            coords.append([lat, lon])
            indexes.append(i)

        if coords:
            return np.array(coords, dtype=float), indexes
        else:
            return np.empty((0, 2)), []

    
    def cluster_results(self, results):
        number_of_days = self.days
        coords, idx = self.get_coordinates(results)
        if coords.size == 0:
            return {"k": 0, "labels": [], "centers": [], "groups": {}, "results": results}
        
        X = np.asarray(coords, dtype = float)
        unique_rows = np.unique(X, axis=0)
        k = min(number_of_days, len(X), len(unique_rows))

        if k <= 1:
            # Trivial: everyone goes to day 0
            for i in idx:
                results[i]["day"] = 0
            return {
                "k": 1,
                "labels": [0] * len(idx),
                "centers": [X.mean(axis=0).tolist()],
                "groups": {0: [results[i] for i in idx]},
                "results": results,
            }
    
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X)
        centers = km.cluster_centers_.tolist()

        # Attach cluster id back to each result
        for j, i in enumerate(idx):
            results[i]["day"] = int(labels[j])

        # Group results by cluster
        groups = {d: [] for d in range(k)}
        for j, i in enumerate(idx):
            groups[int(labels[j])].append(results[i])

        return {
            "k": k,                       # number of clusters
            "labels": [int(l) for l in labels],
            "centers": centers,           # cluster centers [lat, lon]
            "groups": groups,             # dict day -> list of results
            "results": results            # mutated with "day"
        }