import streamlit as st
from streamlit_option_menu import option_menu
import sql_chatbot,rag,temp,email_spam_detector,content_generator,language_translator,sentiment_analyzer,text_classifier,text_summarizer,grammar_correction,invoice
st.set_page_config(page_title="Streamlit App",page_icon="👜")
with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Language Translator","Email Spam Detector","Text Summarizer","Sentiment Analyzer","Grammar Corrector","Text Classifier","Content Generator","Invoice Reader","RAG Chatbot", "SQL DB Chatbot",],
        icons = ["Home","Buger","Home","Home","Home","Home","Home","Home","Home","Home"]
    )

if selected == "RAG Chatbot":
    rag.run()
elif selected == "SQL DB Chatbot":
    sql_chatbot.run()
elif selected == "Language Translator":
    language_translator.run()
elif selected == "Text Summarizer":
    text_summarizer.run()
elif selected == "Sentiment Analyzer":
    sentiment_analyzer.run()
elif selected == "Grammar Corrector":
    grammar_correction.run()
elif selected == "Text Classifier":
    text_classifier.run()
elif selected == "Content Generator":
    content_generator.run()
elif selected == "Invoice Reader":
    invoice.run()
elif selected == "Email Spam Detector":
    email_spam_detector.run()
