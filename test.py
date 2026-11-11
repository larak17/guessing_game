import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError

st.write("To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. To keep track of your incorrect tries, look at the hang man.")

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

# maybe see if we can get it disabled after we pressed start and maybe this could also run a new round?
st.write("Press start to begin the game.")
if st.button("Start"):
    st.write("Game started! Good luck!")

    response = client.responses.create(
    model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
    input="Generate one noun",
)
    st.session_state.word = response.output_text
    st.write(st.session_state.word)


if st.session_state.word:

    letters = list("abcdefghijklmnopqrstuvwxyz")

    # create 3 rows display letters underneath each other
    for row in [letters[:9], letters[9:18], letters[18:]]:
        cols = st.columns(len(row))

        # make each letter a button and disable if pressed
        for i in range(len(row)):
            letter = row[i]

            with cols[i]:
                if st.button(letter, disabled=letter in st.session_state.guessed_letters):
                    st.session_state.guessed_letters.append(letter)
                    st.rerun()


    letters_of_word = list(st.session_state.word.lower()) # we can also do upper, I don't know what makes more sense

    # Check whether the guessed letters are in the given word and display them after each other
    display_word = ""
    for guessed_letter in letters_of_word:
        if guessed_letter in st.session_state.guessed_letters:
            display_word += guessed_letter + " "
        else:
            display_word += " _ "

    st.subheader(display_word)

    if all(letter in st.session_state.guessed_letters for letter in letters_of_word):
        st.write("Congratulations! You guessed the word! Press Start to restart the game.")
        st.balloons


