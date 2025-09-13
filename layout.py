import streamlit as st

def header():
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
            <h1 style='color: #2c3e50;'> AI Travel Agent Assistant </h1>
            <p style='font-size:18px; color: #34495e;'>Your trip planner — built by <b>Emre Çavuş</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_user_inputs(cities):
    col1, col2, col3= st.columns(3)
    with col1:
        location = st.selectbox("Destination", sorted(cities))
    with col2: 
        start_date = st.date_input("Beginning Date", key = "beginning_date")
    with col3: 
        days = st.number_input("Days of Trip", min_value=1, max_value=30, step=1, key="days")
    col4, col5 = st.columns(2)
    with col4:
        budget = st.number_input("Budget (€)", min_value=0, step=50, key="budget")

    with col5:
        preferences = st.multiselect(
            "Select your interests",
            ["Culture", "Food", "Nature", "Shopping", "Nightlife"]
        )

    return location, start_date, days, budget, preferences


def input_checks(location, start_date, days, budget, preferences):
     # --- Validation checks ---
    ready = False
    if not location:
        st.warning("⚠️ Please select a destination before continuing.")
    elif not start_date:
        st.warning("⚠️ Please enter a start date.")
    elif not days or days <= 0:
        st.warning("⚠️ Please specify a valid number of days.")
    elif not budget or budget <= 0:
        st.warning("⚠️ Please enter a valid budget.")
    elif not preferences:
        st.warning("⚠️ Please select at least one preference.")
    else:
        # --- Success block ---
        st.success("✅ Received your inputs")
        ready = True

    return ready


def display_output(output):
    # Access curated places
    curated_clusters = output["clusters"]

    # Access LLM itineraries
    itineraries = output["narratives"]

    for day, text in itineraries.items():
        st.subheader(f"Day {day+1}")
        st.write(text)