import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
import json

st.write("To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. To keep track of your incorrect tries, look at the hang man. Turn on the light mode for better visibility.")

# ── ask for API Key, stop if not yet provided  ────────────────────────────────────────────
with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        type="password",
        key="uos_api_key",
        placeholder="sk-...",
    ).strip()

if not api_key:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=api_key
)

# initializing the session state for the guessed letter and store in list
if "guessed_letters" not in st.session_state:
    st.session_state.guessed_letters = []

# initializing the session state for the generated word and keep it empty first
if "word" not in st.session_state:
    st.session_state.word = ""

# initializing the error count, starting at zero
if "error" not in st.session_state:
    st.session_state.error = 0

if "data_per_game" not in st.session_state:
    st.session_state.data_per_game = []

def save_game():

        # If we want to store all the games that were every played, we have to include this try except statement, otherwise we can also only store it for every starting the web app new
        try:
            with open("game_data.json", "r", encoding="utf-8") as datei:
                all_data = json.load(datei)

        except FileNotFoundError:
            all_data = {"games": []}

        # Determine the next game number
        game_number = len(all_data["games"]) + 1
        
        games = {
            "game": game_number,
            "game_data": st.session_state.data_per_game
        }

        # Append new game
        all_data["games"].append(games)

        # Write updated data
        with open("game_data.json", "w", encoding="utf-8") as datei:
            json.dump(all_data, datei, indent=3, ensure_ascii=False)

# pressing the button Start is the beginning of a new game
st.write("Press Start to begin a new game.")
if st.button("Start"):
    st.session_state.guessed_letters = []
    st.session_state.error = 0
    st.session_state.data_per_game = []
    with st.spinner("Generating new word …"):
        try:
            st.session_state.guessed_letters = []

            response = client.responses.create(
            model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
            instructions="Output one word",
            input="Generate a word that is simple enough for hangman, and has not been generated before",
        )
            st.session_state.word = response.output_text
            st.write("Game started! Good luck!")

        except AuthenticationError:
            st.error("API was not accept. Please check it.")

        except OpenAIError:
            st.error(
                "AI API request failed. Please check it and try again. "
            )
    
#st.info(f"Debug info: The word is {st.session_state.word}.")


if st.session_state.word:

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letters_of_word = list(st.session_state.word.upper()) # we can also do lower, I don't know what makes more sense

    # create 3 rows display letters underneath each other
    for row in [letters[:9], letters[9:18], letters[18:]]:
        cols = st.columns(len(row))

        # make each letter a button and disable if pressed
        for i in range(len(row)):
            letter = row[i]

            with cols[i]:
                if st.button(letter, disabled=letter in st.session_state.guessed_letters):
                    st.session_state.guessed_letters.append(letter)
                    #error count
                    if letter not in letters_of_word:
                        st.session_state.error += 1

                    st.rerun()

    #hangman             
    #st.info(f"Debug info: Error = {st.session_state.error}")
    if st.session_state.error >= 1:
        st.image(
            f"hangman/error{st.session_state.error}.svg",
            caption=f"You made {st.session_state.error} mistake."
        )

    # Pop-up window when the user loses 
    if st.session_state.error >= 10:
        st.session_state.data_per_game = [len(st.session_state.guessed_letters), st.session_state.error, len(st.session_state.word)]
        save_game()
        @st.dialog("Game over!")
        def error_message():
            st.error("Too many tries, you lose!")
            st.write(f"The word was {st.session_state.word}") # show the correct word

            if st.button("New game"):
                st.session_state.word = ""
                st.session_state.guessed_letters = []
                st.session_state.error = 0
                st.session_state.data_per_game = []
                st.rerun()

        error_message()


    # Check whether the guessed letters are in the given word and display them after each other
    display_word = ""
    for guessed_letter in letters_of_word:
        if guessed_letter in st.session_state.guessed_letters:
            display_word += guessed_letter + " "
        else:
            display_word += " _ "

    st.subheader(display_word)

    st.info(f"Guesses: {(len(st.session_state.guessed_letters))}")

    # Pop-up window when the user wins the game
    if all(letter in st.session_state.guessed_letters for letter in letters_of_word):
        st.session_state.data_per_game = [len(st.session_state.guessed_letters), st.session_state.error, len(st.session_state.word)]
        save_game()
        @st.dialog("Game over!")
        def win_message():
            st.success("Congratulations! You guessed the word!")
            st.balloons()
            if st.button("Restart the game"):
                st.session_state.word = ""
                st.session_state.guessed_letters = []
                st.session_state.error = 0
                st.session_state.data_per_game = []
                st.rerun()

        win_message()
    