import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json

st.title("Game Statistics")

# Load data from the json file that got created after the first game
try:
    with open("game_data.json", "r", encoding="utf-8") as datei:
        all_data = json.load(datei)
except: 
    st.info("You have to play at least one game to see your statistics")
    st.stop()

# Create lists for everything that we want to plot
games = []
all_guesses = []
errors = []
word_length = []
guess_quality = []

# loop through each item in the json file and put it into the respective lists
for game in all_data["games"]:
    games.append(game["game"])
    all_guesses.append(game["game_data"][0])
    errors.append(game["game_data"][1])
    word_length.append(game["game_data"][2])
    guess_quality.append(game["game_data"][2] / game["game_data"][0])

# create two counter to display won and lost games
won = 0
lost = 0

# loop through the error count and add games to their respective counter
for error in errors:
    if error == 10:
        lost += 1
    else:
        won += 1

# calculate the average errors and average guesses to display on the stats page
average_errors = sum(errors) / len(games)
average_guesses = sum(all_guesses) / len(games)

# use metric from streamlit to display on the stats page some overall statistics
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
ax.set_ylabel("Guesses")
ax.set_title("Proportion of Wrong Guesses Out of All Guesses")
ax.legend()

plt.tight_layout()
st.pyplot(fig)

information = ''' This Satter Plot shows a possible correlation between word length and wrong guesses. This gives the player the information whether a longer word had more wrong guesses then a shorter word. '''

st.markdown(information)

# Scatter plot: Correlation between word length and wrong guesses
fig2, ax2 = plt.subplots(figsize=(9, 5))

ax2.scatter(
    word_length,
    errors,
    color="cornflowerblue",
    s=80,
    alpha=0.8,
    label="Games"
)

# Trendline for displaying an overall trend of the games played by one person
z = np.polyfit(word_length, errors, 1)
p = np.poly1d(z)

x_line = np.linspace(min(word_length), max(word_length), 100)

ax2.plot(
    x_line,
    p(x_line),
    color="salmon",
    linestyle="--",
    label="Trendline"
)

# Labels and formatting for the plot
ax2.set_xlabel("Word Length")
ax2.set_ylabel("Errors")
ax2.set_title("Word Length vs. Errors")

ax2.grid(alpha=0.3)
ax2.legend()

plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)
