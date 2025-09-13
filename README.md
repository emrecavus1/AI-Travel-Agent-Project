# AI Travel Agent Project

## Overview
This project is an AI-powered travel planning assistant. It generates optimized trip plans based on user preferences, budget, and available days. The system integrates multiple APIs (Google Places, Yelp, OpenStreetMap) and applies clustering techniques to group activities by day. It also leverages a Large Language Model (LLM) agent for personalized itinerary generation.

## Features
- City and category search using Google Places, Yelp, and OSM.  
- Budget integration to control daily expenses.  
- Clustering algorithm (KMeans) to group attractions by day.  
- Hybrid Agent combining:
  - Scoring Agent for evaluating activities.
  - LLM Agent for itinerary creation.  
- Streamlit interface for user interaction.  

## Tech Stack
- **Frontend/UI**: Streamlit  
- **APIs**: Google Places, Yelp, OpenStreetMap  
- **AI/ML**: OpenAI LLM, Scikit-Learn  
- **Environment**: Python 3.12+  

## Project Structure
AI-Travel-Agent-Project/
│── app.py # Streamlit entry point
│── layout.py # UI components
│── helpers.py # Input checks & derived values
│── fetch_data.py # API filtering & integration
│── mappings.py # Preference to category mapping
│── agents/
│ ├── llm_agent.py # LLM integration
│ ├── scoring_agent.py# Scoring mechanism
│ └── hybrid_agent.py # Hybrid pipeline
│── apis/
│ ├── google_places.py
│ ├── yelp.py
│ └── osm.py
│── .env # API keys (not tracked in git)
│── requirements.txt # Dependencies
└── README.md


## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/emrecavus1/AI-Travel-Agent-Project.git
cd AI-Travel-Agent-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```


3. Create a .env file in the project root and add your API keys:
```bash
GOOGLE_PLACES_API=your_google_api_key
YELP_API=your_yelp_api_key
OPENAI_API=your_openai_api_key
```

4. Run the app:
```bash
streamlit run app.py
```

## Usage

Select a city and input your preferences (e.g., culture, food, nature).

Provide budget and trip duration.

The app generates an optimized daily plan with recommendations.

## Roadmap

Add support for multi-city trips

Enhance scoring with user reviews and popularity weights

Save and export plans to PDF

Improve mobile compatibility