from layout import header, get_user_inputs, input_checks, display_output
from helpers import derived_inputs
from agents.hybrid_agent import HybridAgent
from core_modules.fetch_data import APIFilter
import pandas as pd
import streamlit as st

header()
if "cities_df" not in st.session_state:
    st.session_state.cities_df = pd.read_csv("worldcities.csv")

cities_df = st.session_state.cities_df
cities = [f"{row['city_ascii']}, {row['country']}" for _, row in cities_df.iterrows()]
location, start_date, days, budget, preferences = get_user_inputs(cities)
button = st.button("Generate Trip Plan")

if button:
    is_ready = input_checks(location, start_date, days, budget, preferences)
    if is_ready:
        with st.spinner("Generating Trip Plan..."):
            daily_budget, end_date = derived_inputs(start_date, days, budget)
            filter = APIFilter(preferences, daily_budget, location, start_date, end_date, days)
            results = filter.query()
            clusters = filter.cluster_results(results)
            hybrid = HybridAgent(daily_budget=daily_budget, max_places=5)
            output = hybrid.run(clusters)
            display_output(output)
            