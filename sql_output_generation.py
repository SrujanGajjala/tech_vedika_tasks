from langchain_google_genai import ChatGoogleGenerativeAI
gemini_api_key = "AIzaSyAPTR5DUvWct50Tq8sK-iJP3nnraJz2nVs"
model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = gemini_api_key)
import urllib
from langchain_community.utilities import SQLDatabase

user_prompt = "Give me the student ids that have no backlogs"

def get_sql_output(user_prompt,chat_history_text):
    sql_query = generate_sql_query(user_prompt,chat_history_text)
    sql_output = execute_sql_query(sql_query)
    response = final_answer(sql_output,user_prompt)
    return response


def generate_sql_query(user_prompt,chat_history_text):
    prompt = f'''You are a SQL database specialist.
You are a SQL query generator for Microsoft SQL Server. 

You are given a user prompt and a database called `srujandb` with the following tables and schema:

students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    date_of_birth DATE,
    major VARCHAR,
    gpa FLOAT,
    enrollment_year INT
)

no_of_backlogs (
    backlogs INT,
    student_id INT FOREIGN KEY REFERENCES students(student_id)
)

Note: `no_of_backlogs` contains all students, with backlogs ranging from 0 to some number.

Your task is to convert the user's natural language request into a valid SQL query.

📌 Interpretation rule:
- If the user asks something like "how many students have backlogs in mathematics", they mean:
  ➤ Count students **whose major is 'mathematics'** and **whose backlogs > 0**.
  ➤ In SQL terms: join `students` and `no_of_backlogs` on `student_id` and apply the condition on both `major` and `backlogs`.

⚠️ IMPORTANT RULES:
- Return only the raw SQL query — no backticks, no quotes, no markdown formatting.
- Do not include any explanation or preamble.
- Do not add SQL: or ```sql or any such wrappers.
- Just output the SQL query exactly as it would be used in SQL Server.

Conversation History : {chat_history_text}

User request: {user_prompt}
    '''
    response = model.invoke(prompt)
    response_text = response.content
    if response_text.startswith("```"):
        response_text = response_text.replace("```sql", "").replace("```", "")
    # print(response.content)
    return response_text

def execute_sql_query(sql_query):
    db_host = "SRUJAN\SQLEXPRESS"
    db_name = "srujandb"

    # Build connection string
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_host};"
        f"DATABASE={db_name};"
        f"Trusted_Connection=yes;"
    )

    # Initialize the database connection using SQLAlchemy URI
    db = SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={params}")

    # Run the query using LangChain's SQLDatabase
    query = sql_query
    result = db.run(query)
    # print(result)
    return result

def format_sql_output(output):
    if not output:
        return "No results found."

    if isinstance(output, list):
        if all(isinstance(row, tuple) for row in output):
            headers = [f"Column{i+1}" for i in range(len(output[0]))]
            rows = [", ".join(str(item) if item is not None else "NULL" for item in row) for row in output]
            return "\n".join(rows)
        elif all(isinstance(row, dict) for row in output):
            return "\n".join(str(row) for row in output)

    return str(output)


def final_answer(sql_output,user_prompt):
    result_summary = format_sql_output(sql_output)

    prompt = f"""
A user asked: "{user_prompt}"

Here is the result of the SQL query:

{result_summary}

Please respond naturally, using only this output.
"""
    response = model.invoke(prompt)
    return response.content.strip()

# response = get_sql_output(user_prompt)
# print(response)