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
#initialization
if "word" not in st.session_state:
    st.session_state.word = ""
    st.session_state.errors = 0
    st.session_state.display_word = ""
    st.session_state.started = False

# maybe see if we can get it disabled after we pressed start and maybe this could also run a new round?
st.write("Press start to begin the game.")

if st.button("Start"):
    response = client.responses.create(
        model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
        instructions="Output just one word",
        input="Generate a word",
    )
    st.session_state.word = response.output_text
    st.session_state.letters_of_word = list(st.session_state["word"].lower())
    st.session_state.started = True

if st.session_state.started:
    st.write("Game started! Good luck!")
    st.info(st.session_state.letters_of_word)

    for i in st.session_state.letters_of_word:
        st.session_state.display_word+="_ "

    st.subheader(st.session_state.display_word)
 
        # if st.button ("A"):
        #     if "a" in st.session_state.letters_of_word:
        #         st.session_state.display_word+= "A "
        #     else:
        #         st.session_state.errors+=1
        # st.info(st.session_state.errors)


            

        #     if all(letter in display_word for letter in letters_of_word):
        #         st.write("Congratulations! You guessed the word! Press Start to restart the game.")
        #         st.balloons
            #  st.rerun


