import streamlit as st
import matplotlib.pyplot as plt
import json

st.title("Game Statistics")

# Load data from JSON
with open("game_data.json", "r", encoding="utf-8") as datei:
    all_data = json.load(datei)

# Create two lists
games = []
guesses = []

for game in all_data["games"]:
    games.append(game["game"])
    guesses.append(game["game_data"][0])

# Create bar chart
fig, ax = plt.subplots()

ax.bar(games, guesses)
ax.set_xticks(games) # make it only display one number and not a range

ax.set_xlabel("Games")
ax.set_ylabel("Number of guesses")
ax.set_title("Guesses per game")

st.pyplot(fig)