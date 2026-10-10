import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏏 IPL Live Score Dashboard")

# Get API key from secrets.toml
API_KEY = st.secrets["CRICAPI_KEY"]

# API URL
url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

response = requests.get(url)
data = response.json()

if data.get("status") == "success":

    matches = data.get("data", [])

    if matches:
        # Select one match
        match_names = [
            match.get("name", f"Match {i + 1}")
            for i, match in enumerate(matches)
        ]

        selected_match_name = st.selectbox(
            "Select a Match",
            match_names
        )

        selected_index = match_names.index(selected_match_name)
        match = matches[selected_index]

        # Display match details
        st.subheader(match.get("name", "Match Details"))
        st.write("Status:", match.get("status", "Not available"))

        # Get score information
        scores = match.get("score", [])

        if scores:
            teams = []
            runs = []

            for team_score in scores:
                teams.append(team_score.get("inning", "Unknown"))
                runs.append(team_score.get("r", 0))

            # Create DataFrame
            df = pd.DataFrame({
                "Team": teams,
                "Runs": runs
            })

            # Display score table
            st.subheader("📊 Score Table")
            st.dataframe(df, use_container_width=True)

            # Display one graph
            st.subheader("📈 Score Comparison")

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.bar(df["Team"], df["Runs"])
            ax.set_xlabel("Teams")
            ax.set_ylabel("Runs")
            ax.set_title("Score Comparison")
            ax.tick_params(axis="x", rotation=15)

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info("Score data is not available for this match yet.")

    else:
        st.warning("No matches are currently available.")

else:
    st.error("Failed to fetch data. Please check your API key.")
