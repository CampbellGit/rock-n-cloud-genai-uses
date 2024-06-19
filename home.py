import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="🎸",
)

st.write("# Welcome to ROCK & CLOUD! 🎸")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This app is used to demonstrate how easy and quick
    developping generative AI apps can be.

    **👈 Select a demo from the sidebar** to see some examples!
    ### Mandatory sponsorship links?
    - Check out [Daveo](https://www.daveo.fr)
    - Explore streamlit in its [documentation](https://docs.streamlit.io)
    - Learn more about [Langchain](https://www.langchain.com/)
"""
)