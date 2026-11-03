import streamlit as st

st.title("Hang man")

st.subheader("A guessing game by Gwen Sammet and Lara Korte.")

page1 = st.Page("page1.py", title="The Game", icon="🤔")
page2 = st.Page("page2.py", title="The Stats", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()