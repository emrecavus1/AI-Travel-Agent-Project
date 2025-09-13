from agents.scoring_agent import ScoringAgent
from agents.llm_agent import LLMAgent

class HybridAgent:
    """
    Orchestrates the workflow:
    1. Apply scoring agent to trim & rank places under budget
    2. Call LLM agent to generate human-readable itineraries
    """

    def __init__(self, daily_budget: float, max_places: int = 5, model: str = "gpt-4o-mini"):
        self.daily_budget = daily_budget
        self.max_places = max_places
        self.scoring_agent = ScoringAgent(daily_budget=daily_budget, max_places=max_places)
        self.llm_agent = LLMAgent(model=model)

    def curate_clusters(self, clusters: dict) -> dict:
        """
        Run scoring agent on each cluster to select top-N places under budget.
        Returns a new dict with filtered groups.
        """
        curated_groups = {}
        for day, places in clusters["groups"].items():
            curated_groups[day] = self.scoring_agent.select_places(places)

        return {
            "k": clusters["k"],
            "labels": clusters["labels"],
            "centers": clusters["centers"],
            "groups": curated_groups,
            "results": clusters["results"]
        }

    def generate_itineraries(self, clusters: dict) -> dict:
        """
        Call the LLM agent to generate day-by-day narratives
        based on curated clusters.
        """
        return self.llm_agent.generate_itinerary(clusters, self.daily_budget)

    def run(self, clusters: dict) -> dict:
        """
        Full hybrid pipeline:
        1. Curate clusters with scoring agent
        2. Generate itineraries with LLM
        Returns a dict with both curated places and narratives.
        """
        curated = self.curate_clusters(clusters)
        narratives = self.generate_itineraries(curated)

        return {
            "clusters": curated,
            "narratives": narratives
        }
