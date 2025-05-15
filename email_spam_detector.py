import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def run():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)

    st.title("Email Spam Detector")

    #Congratulations! You’ve won a $1000 gift card. Click here to claim now.

    if "email_chat_history" not in st.session_state:
        st.session_state.email_chat_history = []
    
    for qa in st.session_state.email_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])
    
    user_prompt = st.chat_input("Enter the text :")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        chat_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.email_chat_history])
        prompt = f'''You are an email classification assistant. Analyze the following email content and determine whether it is Spam or Not spam.
        Respond in the following exact JSON format:
        {{ "email_type": "Spam" }}
        or
        {{ "email_type": "Not spam" }}
        ### Conversation History : {chat_history_text}
        Email content:{user_prompt}'''

        response = model.invoke(prompt)
        st.session_state.email_chat_history.append({"question":user_prompt,"answer":response.content})
        st.chat_message("assistant").markdown(response.content)

