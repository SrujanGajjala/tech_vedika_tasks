# from dotenv import load_dotenv # type: ignore
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
# from langchain.agents import initialize_agent # type: ignore
# from langchain_community.tools import TavilySearchResults # type: ignore
# from langchain_community.document_loaders import PyPDFLoader # type: ignore
# from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.vectorstores import Chroma
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import pickle
# import streamlit as st

# load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# tavily_api_key = os.getenv("TAVILY_API_KEY")

# model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = gemini_api_key)

# folder_path = r"F:\Tech Vedika\mini_project\Vedika\mini_project\5_pdfs"
# all_docs = []
# text_chunks = []
# chunk_metadata = []

# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path,filename)
#     loader = PyPDFLoader(file_path)
#     docs = loader.load()
#     all_docs.extend(docs)
#     # for doc in docs:
#     #     splitter = RecursiveCharacterTextSplitter(
#     #         chunk_size=3000,
#     #         chunk_overlap=500,
#     #         separators=["\n\n", "\n", " ", ""]  # Better for PDFs
#     #     )
#     #     chunks = splitter.split_text(doc.page_content)
#     #     for chunk in chunks:
#     #         text_chunks.append(chunk)
#     #         chunk_metadata.append({
#     #             'filename' : filename,
#     #             'page' : doc.metadata.get('page',0)
#     #         })

# # print(all_docs)
# texts = ""
# for doc in all_docs:
#     texts+=doc.page_content
# # texts = [doc.page_content for doc in all_docs]

# splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)


# text_chunks = splitter.split_text(texts)

# # print(len(res))
# # print(res[1])
# # print(res)
# # st.write(res)

# os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")





# # from sentence_transformers import SentenceTransformer

# embedding_model =HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
# # embedding_model = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001',google_api_key =gemini_api_key)
# # Extract text from res (which is a list of Document objects)
# # texts = [doc.page_content for doc in res]

# # Embed the texts
# # embeddings = embedding_model.embed_documents(texts)
# vectorstore = FAISS.from_texts(text_chunks, embedding_model)
# # print(len(embeddings))

# with open("faiss_vectorstore.pkl", "wb") as f:
#     pickle.dump(vectorstore, f)


# # vector_index = vectorstore.as_retriever(search_kwargs={'k':6})

# # from langchain.chains import RetrievalQA
# # rag = RetrievalQA.from_chain_type(
# #     llm = model,
# #     chain_type="stuff",
# #     retriever = vector_index,
# #     return_source_documents = True
# # )

# # question = "What are the guiding principles for transition to environmentally sustainable economies and societies?. Do not summarize the points, give as it is from the provided context."
# # response = rag({"query" : question})
# # print(response['result'])

# # question = st.text_area("Question","What are the guiding principles for transition to environmentally sustainable economies and societies?. Do not summarize the points, give as it is from the provided context.?")
# # response = {}

# # if st.button("Submit!"):
# #     response = rag({"query" : question})
# #     st.write("Answer:",response['result'])

# #     if 'source_documents' in response:
# #         st.subheader("Retrieved Chunks :")
# #         for i, doc in enumerate(response['source_documents']):
# #             # Get the original index of this chunk
# #             chunk_index = text_chunks.index(doc.page_content)
# #             metadata = chunk_metadata[chunk_index]
    
# #             st.write(f"\nResult {i+1}:")
# #             st.write(f"File: {metadata['filename']}")
# #             st.write(f"Page: {metadata['page']}")
# #             st.write("Content:")
# #             st.write(doc.page_content)