import streamlit as st

# initializing the session state for the guessed letter and store in list
if "guessed_letters" not in st.session_state:
    st.session_state.guessed_letters = []

word = "Test" # gets generated later by an LLM

st.write("To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. To keep track of your incorrect tries, look at the hang man.")

st.write("Press start to begin the game.")
if st.button("Start"):
    st.write("Game started! Good luck!")

letters = list("abcdefghijklmnopqrstuvwxyz")

# create 3 rows display letters underneath each other
for row in [letters[:9], letters[9:18], letters[18:]]:
    cols = st.columns(len(row))

    # make each letter a button and disable if pressed
    for col, letter in zip(cols, row):
        if col.button(letter, disabled=letter in st.session_state.guessed_letters):
            st.session_state.guessed_letters.append(letter)
            st.rerun()


            #st.session_state.button_disabled = True
            #try1 = letter
            #st.write(f"You guessed: {try1}")


            # if col.button(letter) and letter != try1:
            #     try2 = letter
            #     st.write(f"You guessed: {try2}")

#for i in letters:
# for letter in letters:
#     print(letter)
    # if letter == i in word:
    #     st.write(f"{i} is in the word!")