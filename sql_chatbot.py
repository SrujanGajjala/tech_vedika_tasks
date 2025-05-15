import streamlit as st
import sql_output_generation

def run():
    st.title("SQL Chatbot")

    if "sql_chat_history" not in st.session_state:
        st.session_state.sql_chat_history = []

    for qa in st.session_state.sql_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])

    user_prompt = st.chat_input("What do u want to retrieve from the database ?")

    if user_prompt:
        with st.spinner("Generating response..."):
            response = sql_output_generation.get_sql_output(user_prompt)
        st.chat_message("user").markdown(user_prompt)
        st.chat_message("assistant").markdown(response)
        st.session_state.sql_chat_history.append({"question" : user_prompt,"answer" : response})


