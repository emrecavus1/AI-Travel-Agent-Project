from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
openai_key = os.getenv("OPENAI_API")
class LLMAgent:
    def __init__(self, model: str = "gpt-4o-mini", max_tokens: int = 800):
        if not openai_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API in your .env")
        self.client = OpenAI(api_key=openai_key)
        self.model = model
        self.max_tokens = max_tokens

    def _format_day_prompt(self, day: int, places: list, daily_budget: float) -> str:
        """
        Build a structured prompt for a single day.
        """
        place_list = []
        for p in places:
            place_list.append(
                f"- {p.get('name')} "
                f"(Category: {p.get('source')}, "
                f"Price ~€{p.get('price', 0)}, "
                f"Rating {p.get('rating', 'N/A')} "
                f"with {p.get('review_count', 0)} reviews)"
            )

        prompt = f"""
        You are a travel assistant. Your task is to create a curated day {day+1} itinerary
        using the following candidate places. Respect the daily budget of ~€{daily_budget},
        prefer highly rated places, and ensure diversity (e.g., culture + food + nature if possible).

        Here are the candidates for Day {day+1}:
        {chr(10).join(place_list)}

        Now, produce a human-friendly narrative itinerary for the day, with 3-5 activities max.
        Mention the names of the places chosen, why they are good picks, and keep the total
        approximate spend under the daily budget.
        """
        return prompt.strip()

    def generate_itinerary(self, clusters: dict, daily_budget: float) -> dict:
        """
        For each cluster/day, ask the LLM to generate a narrative.
        Returns a dict: day -> itinerary text
        """
        narratives = {}

        for day, places in clusters["groups"].items():
            if not places:
                narratives[day] = f"Day {day+1}: No activities available."
                continue

            prompt = self._format_day_prompt(day, places, daily_budget)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful travel planning assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=0.7,
            )

            text = response.choices[0].message.content.strip()
            narratives[day] = text

        return narratives