import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json

st.title("Game Statistics")

# Load data from JSON
with open("game_data.json", "r", encoding="utf-8") as datei:
    all_data = json.load(datei)

# Create two lists
games = []
all_guesses = []
errors = []
word_length = []
guess_quality = []


for game in all_data["games"]:
    games.append(game["game"])
    all_guesses.append(game["game_data"][0])
    errors.append(game["game_data"][1])
    word_length.append(game["game_data"][2])
    guess_quality.append(game["game_data"][2] / game["game_data"][0])

won = 0
lost = 0

for error in errors:
    if error == 10:
        lost += 1
    else:
        won += 1

average_errors = sum(errors) / len(games)
average_guesses = sum(all_guesses) / len(games)

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Games Won", value=won)
col2.metric(label="Games Lost", value=lost)
col3.metric(label="Average Guesses", value=average_guesses)
col4.metric(label="Average Errors", value=average_errors)

# Bar Plot: Guesses and Errors
fig, ax = plt.subplots(figsize=(10, 5))

bar1 = ax.bar(games, all_guesses, label="All Guesses",
              color="cornflowerblue")

bar2 = ax.bar(games, errors, label="Errors",
              color="salmon")

ax.set_xticks(games)
ax.set_xlabel("Games")
ax.set_ylabel("Number")
ax.set_title("Proportion of Wrong Guesses per Game")
ax.legend()

plt.tight_layout()
st.pyplot(fig)


# Bar Plot: Guess Quality
fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(games, guess_quality, width=1,
       color="mediumseagreen")

ax.set_xticks(games)
ax.set_xlabel("Games")
ax.set_ylabel("Word Length Divided by all Guesses")
ax.set_title("Guess Quality per Game")

plt.tight_layout()
st.pyplot(fig)


# Pie Chart: Won vs. Lost
fig, ax = plt.subplots(figsize=(7, 5))

ax.pie(
    [won, lost],
    labels=["Games Won", "Games Lost"],
    colors=["mediumseagreen", "salmon"],
    autopct="%1.1f%%"
)

ax.set_title("Won vs. Lost Games")

plt.tight_layout()
st.pyplot(fig)
