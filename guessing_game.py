import streamlit as st

st.set_page_config(page_title="Hangman")
st.logo("hangman/error10.svg")
st.title("Hangman")

st.subheader("This is the first project for the course AI and the Web")
st.markdown("A project by Gwendolin Sammet and Lara Korte.")

page1 = st.Page("page1.py", title="The Game", icon="🤔")
page2 = st.Page("page2.py", title="The Stats", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()