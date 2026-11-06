import streamlit as st

st.write("To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. To keep track of your incorrect tries, look at the hang man.")

# maybe see if we can get it disabled after we pressed start and maybe this could also run a new round?
st.write("Press start to begin the game.")
if st.button("Start"):
    st.write("Game started! Good luck!")

# initializing the session state for the guessed letter and store in list
if "guessed_letters" not in st.session_state:
    st.session_state.guessed_letters = []

# variables that are needed for the game
word = "Test" # gets generated later by an LLM
letters_of_word = list(word.lower()) # we can also do upper, I don't know what makes more sense
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

# Check whether the guessed letters are in the given word and display them after each other
display_word = ""
for guessed_letter in letters_of_word:
    if guessed_letter in st.session_state.guessed_letters:
        display_word += guessed_letter + " "
    else:
        display_word += " _ "

st.subheader(display_word)


