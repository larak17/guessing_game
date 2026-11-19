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

# Scatter plot
fig2, ax2 = plt.subplots(figsize=(9, 5))

ax2.scatter(
    word_length,
    all_guesses,
    color="cornflowerblue",
    s=80,
    alpha=0.8,
    label="Games"
)

# Trendline
z = np.polyfit(word_length, all_guesses, 1)
p = np.poly1d(z)

x_line = np.linspace(min(word_length), max(word_length), 100)

ax2.plot(
    x_line,
    p(x_line),
    color="salmon",
    linestyle="--",
    label="Trendline"
)

# Labels and formatting
ax2.set_xlabel("Word Length")
ax2.set_ylabel("All Guesses")
ax2.set_title("Word Length vs. Number of Guesses")

ax2.grid(alpha=0.3)
ax2.legend()

plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)