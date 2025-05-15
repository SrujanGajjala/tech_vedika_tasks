import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
import urllib

def run():
    gemini_api_key = "AIzaSyAPTR5DUvWct50Tq8sK-iJP3nnraJz2nVs"
    llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", api_key = gemini_api_key)

    db_host = "SRUJAN\SQLEXPRESS"
    db_name = "srujandb"  # Replace with your DB name
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_host};"
        f"DATABASE={db_name};"
        f"Trusted_Connection=yes;"
    )
    db = SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={params}")

    toolkit = SQLDatabaseToolkit(db = db,llm=llm);
    agent_executor = create_sql_agent(
        llm = llm,
        toolkit = toolkit,
        verbose = True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )

    # answer = agent_executor.invoke("Give me the the student names that have no backlogs")
    # answer = agent_executor.invoke({"input":"Give me the the student names greater than 3.8 cgpa and enrolled in year 2020. While searching, don't put the sql statements in multiline string since it is already enclosed in a string."})

    if "sql_chat_history" not in st.session_state:
        st.session_state.sql_chat_history = []

    st.title("🛢️ SQL DB Chatbot")

    # Display chat history
    for qa in st.session_state.sql_chat_history:
        st.chat_message("user").markdown(qa["question"])
        st.chat_message("assistant").markdown(qa["answer"])

    # User input
    user_prompt = st.chat_input('Ask about all invoices...')
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        # Build conversation history
        sql_history_text = "\n".join([f"User: {qa['question']}\nAI: {qa['answer']}" for qa in st.session_state.sql_chat_history])

        prompt = f"""
        You are a helpful assistant that can access and query a SQL database.

        When you decide what to do, follow this format:
        Thought: [your reasoning here]
        Action: query_sql_db
        Action Input: [the SQL query here]

        Only use tools you are provided with. If you know the answer without querying, you can just respond with the answer.

        ### Conversation History:
        {sql_history_text}

        ### New Question:
        {user_prompt}
        """
        # Get response from Gemini
        try:
            gemini_response = agent_executor.invoke({"input": prompt})
            cnt = 0
            while cnt<3 and gemini_response['output']!="I don't know":
                gemini_response = agent_executor.invoke({"input": prompt})
                cnt+=1
            
            assistant_response = gemini_response['output'] or "Sorry, I couldn't generate a response."
        except ValueError:
            assistant_response = "There was an issue processing your request. Please try again later."

        # Store in chat history
        st.session_state.sql_chat_history.append({"question": user_prompt, "answer": assistant_response})

        # Display response
        st.chat_message("assistant").markdown(assistant_response)