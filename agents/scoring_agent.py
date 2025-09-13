import math
from typing import List, Dict

class ScoringAgent:
    def __init__(self, daily_budget: float, max_places: int):
        self.daily_budget = daily_budget
        self.max_places = max_places

    def score_place(self, place: Dict) -> float:
        """
        Compute a score for a place.
        Factors:
        - rating (higher is better)
        - review_count (confidence in rating)
        - lower price is preferred
        """
        rating = place.get("rating", 0) or 0
        review_count = place.get("review_count", 0) or 0
        price = place.get("price", 0) or 0

        # Weighting logic
        rating_weight = 2.0
        review_weight = 0.3
        price_penalty = 0.05

        score = (rating * rating_weight) \
              + (math.log1p(review_count) * review_weight) \
              - (price * price_penalty)

        return score
    

    def select_places(self, places: List[Dict]) -> List[Dict]:
        """
        Select top places under the daily budget.
        - Sort by score
        - Iteratively add until budget or max_places reached
        """
        scored_places = [(p, self.score_place(p)) for p in places]
        scored_places.sort(key=lambda x: x[1], reverse=True)

        selected, total_cost = [], 0
        for place, score in scored_places:
            price = place.get("price", 0) or 0
            if len(selected) >= self.max_places:
                break
            if total_cost + price <= self.daily_budget:
                place["score"] = score
                selected.append(place)
                total_cost += price

        return selected