import streamlit as st

st.write("To play the game, try to guess the word by suggesting letters. You have a limited number of incorrect guesses before the game is over. To keep track of your incorrect tries, look at the hang man.")

st.write("Press start to begin the game.")
if st.button("Start"):
    word = "Test"
    st.write("Game started! Good luck!")
    
for i in range(len(word)):
    st.write("_")

#Display letters
letters = list("abcdefghijklmnopqrstuvwxyz")

# create 3 rows display letters underneath each other
for row in [letters[:9], letters[9:18], letters[18:]]:
    cols = st.columns(len(row))

    # make each letter a button
    for col, letter in zip(cols, row):
        col.button(letter)
