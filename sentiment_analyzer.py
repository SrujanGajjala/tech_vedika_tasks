import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def run():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)

    st.title("Sentiment Analyzer")

    #Congratulations! You’ve won a $1000 gift card. Click here to claim now.

    if "senti_chat_history" not in st.session_state:
        st.session_state.senti_chat_history = []
    
    for qa in st.session_state.senti_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])
    
    user_prompt = st.chat_input("Enter the text :")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        chat_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.senti_chat_history])
        prompt = f'''You are a sentiment analysis assistant.
        Determine the sentiment of the following review.
        Respond only in this exact JSON format:
        {{ "review": "POSITIVE" }}
        {{ "review": "NEGATIVE" }}
        {{ "review": "NEUTRAL" }}
        Review text:{user_prompt}
        ### Conversation History : {chat_history_text}
        '''

        response = model.invoke(prompt)
        st.session_state.senti_chat_history.append({"question":user_prompt,"answer":response.content})
        st.chat_message("assistant").markdown(response.content)


# gemini_api_key = os.getenv("GEMINI_API_KEY")
# model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)

# prompt = input("Enter the text :")

# #Congratulations! You’ve won a $1000 gift card. Click here to claim now.

# response = model.invoke(
#     f'''You are a sentiment analysis assistant.
# Determine the sentiment of the following review.

# Respond only in this exact JSON format:

# {{ "review": "POSITIVE" }}
# {{ "review": "NEGATIVE" }}
# {{ "review": "NEUTRAL" }}

# Review text:{prompt}'''
# )

# print(response.content)