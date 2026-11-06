import streamlit as st

st.title("Hangman")

st.subheader("This is the first project for the cours AI and the Web")

page1 = st.Page("page1.py", title="The Game", icon="🤔")
page2 = st.Page("page2.py", title="The Stats", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()