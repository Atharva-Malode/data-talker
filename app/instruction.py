import streamlit as st

def instructions():
    with st.sidebar.expander("Instructions"):
        st.markdown("1. Enter your OpenAI API key")
        st.markdown("2. Upload a CSV file")
        st.markdown("3. Input queries and see responses")
    st.sidebar.info("Note : We are working on introducing the LLAMA model by Meta AI for better results which would not need any API key. Please feel free to contact us for any queries, we would also appreciate open source contributions and sponsors.")
    github_link = "[GitHub](https://github.com/Atharva-Malode/Data-Talker)"
    st.sidebar.info("To contribute and Sponser - " + github_link)