import streamlit as st
from chainstream.pages import environment, documents, chatbot


st.set_page_config(page_title="Chatbot", page_icon="💬")
page_names_to_funcs = {
    "Environment Setup": environment.demo,
    "Import documents": documents.demo,
    "Chatbot": chatbot.demo,
}
demo_name = st.sidebar.selectbox("Naviagate Pages", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
