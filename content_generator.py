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

    st.title("Content Generator")

    #Congratulations! You’ve won a $1000 gift card. Click here to claim now.
    topic = st.text_input("Enter the topic:")
    specifications = st.text_input("Enter the specifications :")
    submitted = st.button("Submit")
    if "content_chat_history" not in st.session_state:
        st.session_state.content_chat_history = []
    
    for qa in st.session_state.content_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])
    
    

    if submitted:
        chat_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.content_chat_history])
        prompt = f'''You are a content generator assistant.
        Based on the topic and specifications generate content related to it.
        Topic:{topic}
        Specifications : {specifications}
        ### Conversation History : {chat_history_text}
        '''
        with st.spinner("Generating response..."):
            response = model.invoke(prompt)
        st.session_state.content_chat_history.append({"question":topic+specifications,"answer":response.content})
        st.chat_message("assistant").markdown(response.content)

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# model = ChatGoogleGenerativeAI(model ="gemini-2.0-flash",api_key = gemini_api_key)

# topic = input("Enter the topic :")
# specifications = input("Enter the specifications: ")
# # Artificial Intelligence
# # Introduction, Benefits, Challenges, Future Trends etc 
# response = model.invoke(
#     f'''You are a content generator assistant.
#     Based on the topic and specifications generate content related to it.
# Topic:{topic}
# Specifications : {specifications}'''
# )
# print(response.content)