import streamlit as st
import sql_output_generation
from langchain_google_genai import ChatGoogleGenerativeAI
gemini_api_key = "AIzaSyAPTR5DUvWct50Tq8sK-iJP3nnraJz2nVs"
model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = gemini_api_key)
def run():
    st.title("SQL Chatbot")

    if "sql_chat_history" not in st.session_state:
        st.session_state.sql_chat_history = []

    for qa in st.session_state.sql_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])

    user_prompt = st.chat_input("What do u want to retrieve from the database ?")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        sql_chat_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.sql_chat_history])
        

        with st.spinner("Generating response..."):
            response = sql_output_generation.get_sql_output(user_prompt,sql_chat_history_text)
        
        st.chat_message("assistant").markdown(response)
        st.session_state.sql_chat_history.append({"question" : user_prompt,"answer" : response})




#         prompt = f"""
# You are a SQL database specialist and a helpful assistant.

# The user has asked the following question:
# "{user_prompt}"

# A language model has already generated the following response:
# "{final_answer}"

# Here is the conversation history for reference:
# {sql_chat_history_text}

# ✅ Your task:
# - Review the user's question and the model-generated answer.
# - Use the conversation history for context.
# - Return a clear, final chatbot-style response that is natural, conversational, and helpful.
# - Do NOT fabricate any data. Use only what is present in the final answer or previously known from history.
# - If the final answer is incorrect or incomplete, politely inform the user that the response may not be accurate, and suggest they rephrase the question if needed.

# 🎯 Your response should be:
# - Friendly, clear, and human-like
# - Grounded strictly in the data available
# - Tailored specifically to the user's request
#         """