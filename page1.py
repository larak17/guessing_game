import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
import json

intro = ''' To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. If you know the whole word, type it into the field on the bottom to reduce the amount of your guesses.  
  
:warning: **To keep track of your incorrect tries, look at the hangman showing up in the sidebar.**  
  
*Tip: Turn on the light mode for better visibility.*
'''
st.markdown(intro)

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

# initializing the session state variables
if "guessed_letters" not in st.session_state:
    st.session_state.guessed_letters = []

if "word" not in st.session_state:
    st.session_state.word = ""

if "word_list" not in st.session_state:
    st.session_state.word_list = []

if "error" not in st.session_state:
    st.session_state.error = 0

if "data_per_game" not in st.session_state:
    st.session_state.data_per_game = []

if "word_input" not in st.session_state: 
    st.session_state.word_input = ""

# Store data in json file for statistics
def save_game():
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

# Use LLM to generate word
def word_generation():
    with st.spinner("Generating new word …"):
            try:
                st.session_state.guessed_letters = []

                response = client.responses.create(
                model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
                instructions="Output one word",
                input="Generate a word that is simple enough for hangman and has at least 5 letters.",
            )
                new_word = response.output_text.upper()

                # prevent repetition of generated word
                if new_word in st.session_state.word_list:
                    response = client.responses.create(
                        model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
                        instructions="Output one word",
                        input=f"Generate a word for hangman that is not included in {st.session_state.word_list}."
                    )
                    new_word = response.output_text.upper()

                st.session_state.word = new_word
                st.session_state.word_list.append(new_word)
                st.write("Game started! Good luck!")

            except AuthenticationError:
                st.error("API was not accept. Please check it.")

            except OpenAIError:
                st.error(
                    "AI API request failed. Please check it and try again. "
                )

# pressing the button Start is the beginning of a new game
st.write("Press Start to begin a new game.")
if st.button("Start"):
    st.session_state.guessed_letters = []
    st.session_state.error = 0
    st.session_state.data_per_game = []
    word_generation()

# Presenting letters etc. after word is generated
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

    
    # Check whether the guessed letters are in the given word and display them after each other
    display_word = ""
    for guessed_letter in letters_of_word:
        if guessed_letter in st.session_state.guessed_letters:
            display_word += guessed_letter + " "
        else:
            display_word += " _ "

    st.subheader(display_word)

    # Hangman visualization             
    if st.session_state.error >= 1:
        st.sidebar.image(
            f"hangman/error{st.session_state.error}.svg",
            caption=f"You made {st.session_state.error} mistake."
        )

    # Opportunity for text input to reduce guesses, if user knows word already
    prompt = st.chat_input("Guess the whole word")
    if prompt:
        st.session_state.word_input = prompt.upper()
        st.session_state.guessed_letters.append("ö")
        if st.session_state.word_input != st.session_state.word.upper():
            st.write("Try again")
            st.session_state.error += 1
            st.rerun()
        
    st.info(f"Guesses: {len((st.session_state.guessed_letters))}")

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
                st.session_state.word_input = ""
                st.rerun()

        error_message()

    # Pop-up window when the user wins the game
    if all(letter in st.session_state.guessed_letters for letter in letters_of_word) or st.session_state.word_input == st.session_state.word.upper():
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
                st.session_state.word_input = ""
                st.rerun()

        win_message()

 