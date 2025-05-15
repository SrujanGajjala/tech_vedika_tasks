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

    st.title("Text Classifier")

    #Congratulations! You’ve won a $1000 gift card. Click here to claim now.

    if "classifier_chat_history" not in st.session_state:
        st.session_state.classifier_chat_history = []
    
    for qa in st.session_state.classifier_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])
    
    user_prompt = st.chat_input("Enter the text :")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        chat_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.classifier_chat_history])
        prompt = f'''You are a text classification assistant.
        Classify the following text into one of the predefined labels: Technology, Finance, Medical, or Agriculture.
        Return the result in a table-like format with the following columns:
        Text
        Label
        The categories are:
        Technology
        Finance
        Medical
        Agriculture
        Text to classify:{user_prompt}
        ### Conversation History : {chat_history_text}
        '''

        with st.spinner("Generating response..."):
            response = model.invoke(prompt)
        st.session_state.classifier_chat_history.append({"question":user_prompt,"answer":response.content})
        st.chat_message("assistant").markdown(response.content)


















# gemini_api_key = os.getenv("GEMINI_API_KEY")
# model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)

# prompt = input("Enter the text :")

# #Apple has launched a new AI-powered chip that enhances mobile performance. 

# response = model.invoke(
#     f'''You are a text classification assistant.
# Classify the following text into one of the predefined labels: Technology, Finance, Medical, or Agriculture.

# Return the result in a table-like format with the following columns:

# Text

# Label

# The categories are:

# Technology

# Finance

# Medical

# Agriculture

# Text to classify:{prompt}'''
# )

# print(response.content)