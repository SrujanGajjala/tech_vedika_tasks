import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

config = load_config()


def run():
    gemini_api_key = config["GEMINI_API_KEY"]
    model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)
    st.title("Language Detector and Translator")

    selected_option = st.selectbox("Choose what u want to do :",["Detector","Translator"])
    if selected_option == "Detector":
        user_prompt = st.chat_input("Enter the text :")
        if user_prompt:
            prompt = f'''Detect the language of the following text and respond only with the name of the language.
            Here's the text : {user_prompt}'''
            with st.spinner("Generating response..."):
                response = model.invoke(prompt)
            st.write(response.content)
    
    elif selected_option == "Translator":
        user_prompt = st.chat_input("Enter the text :")
        if user_prompt:
            prompt = f'''Translate the following text to english and return it.
            Here's the text : {user_prompt}'''
            with st.spinner("Generating response..."):
                response = model.invoke(prompt)
            st.write(response.content)




