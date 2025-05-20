import pickle
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import streamlit as st
import json
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

config = load_config()

def run():
    gemini_api_key = config["GEMINI_API_KEY"]
    model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = gemini_api_key)
    # Load vector store from pickle file
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    loaded_vectorstore = FAISS.load_local("faiss_index", embeddings=embedding_model,allow_dangerous_deserialization=True)
    # with open("faiss_vectorstore.pkl", "rb") as f:
    #     loaded_vectorstore = pickle.load(f)

    # Optional: test search
    # query = "Which governments attempted to undermine the vital independence of the trade union movement through laborious registration procedures?"
    # results = loaded_vectorstore.similarity_search(query, k=3)
    vector_index = loaded_vectorstore.as_retriever(search_kwargs={'k':3})

    # print(vector_index)
    from langchain.chains import RetrievalQA
    rag = RetrievalQA.from_chain_type(
        llm = model,
        chain_type="stuff",
        retriever = vector_index,
        return_source_documents = True
    )

    # question = "Which governments attempted to undermine the vital independence of the trade union movement through laborious registration procedures?"
    # question = "What are the guiding principles for transition to environmentally sustainable economies and societies?"
    # question = st.text_area("Question","Ask Question to LLM")
    # response = {}

    # if st.button("Submit!"):
    #     response = rag({"query" : question})
    #     st.write("Answer:",response['result'])

    st.title("RAG ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Ask Question to LLM"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.spinner("Generating response..."):
            response = rag({"query":prompt})
        
        
        with st.chat_message("assistant"):
            st.markdown(response['result'])
        
        st.session_state.messages.append({"role":"assistant","content":response['result']})





















# st.write("Retrieved Chunks:")
# for i, doc in enumerate(vector_index):
#     # Get the original index of this chunk
#     chunk_index = text_chunks.index(doc.page_content)
#     metadata = chunk_metadata[chunk_index]
    
#     print(f"\nResult {i+1}:")
#     print(f"File: {metadata['filename']}")
#     print(f"Page: {metadata['page']}")
#     print("Content:")
#     print(doc.page_content)

# response = rag({"query" : question})
# print(response['result'])
# st.write(response)
# for i,doc in enumerate(response["source_documents"]):
#     st.write(f"--- Document {i} ---")
#     st.write(doc.page_content)
#     st.write(f"Source: {doc.metadata['source']}, Page: {doc.metadata.get('page', 'N/A')}\n")

# st.write("Sources:")
# for doc in response["source_documents"]:
#     metadata = doc.metadata
#     source_file = os.path.basename(metadata.get('source', 'Unknown file'))
#     page_number = metadata.get('page', 'Unknown page')
#     st.write(f"📄 File: {source_file}, 📄 Page: {page_number}")

