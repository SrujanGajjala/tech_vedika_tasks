import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyMuPDFLoader
import streamlit as st
import tempfile
import json
import re
import json

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

config = load_config()

load_dotenv()
def run():
  gemini_api_key = config["GEMINI_API_KEY"]

  model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = gemini_api_key,temperature = 0)

  st.title("Doc to JSON Converter")

  uploaded_file = st.file_uploader("Choose a File")
  if uploaded_file is not None:
      # Save to a temporary file
      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
          tmp.write(uploaded_file.getbuffer())
          tmp_path = tmp.name  # Save the path
      
      # Load PDF
      loader = PyMuPDFLoader(tmp_path)
      docs = loader.load()
      # Optionally delete temp file after use
      text = "\n\n".join([doc.page_content for doc in docs])
      prompt = f"""
  You are an intelligent invoice parsing system.

  Your job is to extract structured data from raw, unformatted invoice text.

  The invoice text may be messy, lack labels, and have mixed ordering of information — your task is to interpret and extract meaning as accurately as possible.

  ### Your Response Must:
  - Follow the exact JSON schema shown below.
  - Include **all fields**, even if data is partial or slightly ambiguous.
  - Leave a field empty ONLY if the data is truly missing.
  - Return **ONLY the JSON object** — no extra text or explanation.

  ### JSON Template:
  {{
    "invoice_details": {{
      "invoice_number": "",
      "order_number": "",
      "invoice_date": "",
      "due_date": "",
      "total_due": ""
    }},
    "sender": {{
      "name": "",
      "address": "",
      "email": ""
    }},
    "recipient": {{
      "name": "",
      "address": "",
      "email": ""
    }},
    "line_items": [
      {{
        "quantity": "",
        "service": "",
        "description": "",
        "rate_price": "",
        "adjust": "",
        "sub_total": ""
      }}
    ],
    "summary": {{
      "sub_total": "",
      "tax": "",
      "total": ""
    }},
    "payment_information": {{
      "bank_name": "",
      "account_number": "",
      "bsb": "",
      "status": ""
    }},
    "terms": ""
  }}

  ### Instructions:
  - Infer values where formatting is unclear (e.g., numbers near service names may be quantities/rates).
  - Use surrounding context to map values (e.g., “ANZ Bank” is likely the bank name).
  - Return field values as strings, even if they're numbers.
  - Do not change key names.
  - Do not omit any keys, even if values are blank.

  Now extract structured JSON from the following invoice text:

  {text}
  """
      with st.spinner("Generating response..."):
            response = model.invoke(prompt)
      # st.write(text)
      st.subheader("JSON Format:")
      st.write(response.text())

      json_text = response.text()
      cleaned_text = re.sub(r"^```(?:json)?|```$", "", json_text.strip(), flags=re.MULTILINE)
      parsed = json.loads(cleaned_text)
      sub_total = float(parsed["summary"]["sub_total"][1:])
      tax = float(parsed["summary"]["tax"][1:])
      total = float(parsed["summary"]["total"][1:])

      if total == tax+sub_total:
          st.success("Sum of sub_Total, tax is equal to Total")
      else:
          st.error("Sum of Sub_Total, Tax is not equal to Total")
          st.error("sub_total + tax != total")

      os.remove(tmp_path)



# Read all the values without missing any from the given text.

# Make sure there are no null values, leave them null if and only if u there is no relevant value to fit into that key.
# Try to read all the values with all font sizes, dont miss any.
# Read each and every character, dont miss any. Check all the keys containing null values again and again, if there's any possible value that can be fitted into that key then do that.



#     response = model.invoke(["""Extract the following text into a structured JSON format:{
#   "invoice_details": {
#     "invoice_number": "",
#     "order_number": "",
#     "invoice_date": "",
#     "due_date": "",
#     "total_due": ""
#   },
#   "sender": {
#     "name": "",
#     "address": "",
#     "email": ""
#   },
#   "recipient": {
#     "name": "",
#     "address": "",
#     "email": ""
#   },
#   "line_items": [
#     {
#       "quantity": "",
#       "service": "",
#       "description": "",
#       "rate_price": "",
#       "adjust": "",
#       "sub_total": ""
#     }
#   ],
#   "summary": {
#     "sub_total": "",
#     "tax": "",
#     "total": ""
#   },
#   "payment_information": {
#     "bank_name": "",
#     "account_number": "",
#     "bsb": "",
#     "status": ""
#   },
#   "terms": ""
# }
# . Give me with these keys only.
# Fill all the values accurately do not show any inconsistencies.
# Double Check for all keys with the values from the given text if any value can be fitted into that key.
# """,text])

