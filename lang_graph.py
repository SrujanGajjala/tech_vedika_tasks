from langgraph.graph import MessageGraph,END
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
import streamlit as st

model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",api_key = "AIzaSyAPTR5DUvWct50Tq8sK-iJP3nnraJz2nVs")
search = TavilySearchResults(tavily_api_key = "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")


def product_analyzer_node(state):
    user_input = state[-1].content
    prompt = (
        "You are a product analyst. Based on the user_input, give me an in depth analysis of the product."
    )
    response = model.invoke(
        [
            HumanMessage(content = prompt),
            HumanMessage(content = user_input)
        ]
    )
    return state + [AIMessage(content = response.content)]

def generating_search_query(state):
    product_analysis = state[-1].content
    prompt = (
        """
        Based on the analysis of this product, generate a concise search engine query (no more than 1 to 2 lines) that I can use to find its top competitors or alternative products. Do not include explanations — just output the search query.
        """
    )
    response = model.invoke(
        [
            HumanMessage(content = prompt),
            HumanMessage(content = product_analysis)
        ]
    )
    return state + [AIMessage(content = response.content)]

def searching_for_competitors(state):
    search_query = state[-1].content
    search_results = search.invoke(search_query)
    print(search_results)
    response = model.invoke(f"""
    You are a business analyst. Carefully review the following search results and extract only the names of prominent competitors or alternative products/services to the one being analyzed. 
    List only well-known or relevant competitors — avoid irrelevant mentions, descriptions, or background info.

    Search Results:
    {search_results}
    """)
    return state + [AIMessage(content = response.content)]

def competitor_analysis(state):
    competitors = state[-1].content
    prompt = (
        "Give me an indepth analysis of the following competitors"
    )
    response = model.invoke(
        [
            HumanMessage(content = prompt),
            HumanMessage(content = competitors)
        ]
    )
    return state + [AIMessage(content = response.content)]

def marketing_strategy(state):
    product_analysis = state[1].content
    competitor_analysis = state[-1].content
    prompt = f"""
    You are a smart marketing strategist.

    Below is the analysis of a product and its competitors. Based on both, suggest effective marketing strategies to improve and promote the product.

    ## Product Analysis:
    {product_analysis}

    ## Competitor Analysis:
    {competitor_analysis}

    Return concise, actionable marketing strategies in bullet points. Avoid repeating the input content.
    """

    response = model.invoke([HumanMessage(content=prompt)])
    return state + [AIMessage(content = response.content)]

def email_generation(state):
    marketing_strategy = state[-1].content
    prompt = (
        "You are a smart email generator. Based on the marketing strategy, generate an email that promotes my product."
    )
    response = model.invoke(
        [
            HumanMessage(content = prompt),
            HumanMessage(content = marketing_strategy)
        ]
    )
    return state + [AIMessage(content = response.content)]

def social_media_post(state):
    marketing_strategy = state[-2].content
    prompt = (
        "You are a social media post generator. Based on the marketing strategy, generate a post that promotes my product."
    )
    response = model.invoke(
        [
            HumanMessage(content = prompt),
            HumanMessage(content = marketing_strategy)
        ]
    )
    return state + [AIMessage(content = response.content)]

def build_graph():
    graph = MessageGraph()
    graph.add_node("Product Analyzer", product_analyzer_node)
    graph.add_node("Search Query Generator", generating_search_query)
    graph.add_node("Searching Competitors", searching_for_competitors)
    graph.add_node("Competitor Analyzer", competitor_analysis)
    graph.add_node("Marketing Strategy", marketing_strategy)
    graph.add_node("Email Generator", email_generation)
    graph.add_node("Social Media Post Generator", social_media_post)
    graph.set_entry_point("Product Analyzer")
    graph.add_edge("Product Analyzer","Search Query Generator")
    graph.add_edge("Search Query Generator","Searching Competitors")
    graph.add_edge("Searching Competitors","Competitor Analyzer")
    graph.add_edge("Competitor Analyzer","Marketing Strategy")
    graph.add_edge("Marketing Strategy","Email Generator")
    graph.add_edge("Email Generator","Social Media Post Generator")
    agent = graph.compile()
    return agent

def run():
    user_input = st.text_input("Give the product :")

    # Build the graph only once
    if "agent" not in st.session_state:
        st.session_state.agent = build_graph()

    # Only run once on initial input
    if user_input and (
        "user_input" not in st.session_state or st.session_state.user_input != user_input
    ):
        with st.spinner("Analyzing..."):
            st.session_state.agent_response = st.session_state.agent.invoke([HumanMessage(content=user_input)])
            st.session_state.user_input = user_input  # Save latest input

    # Show buttons (only if response exists)
    if "agent_response" in st.session_state:
        col1, col2, col3, col4, col5 = st.columns(5)
        final_report = ""
        with col1:
            if st.button("Product Analysis"):
                final_report = st.session_state.agent_response[1].content
                st.write()
        with col2:
            if st.button("Competitor Analysis"):
                final_report = st.session_state.agent_response[4].content
        with col3:
            if st.button("Marketing Strategy"):
                final_report = st.session_state.agent_response[5].content
        with col4:
            if st.button("Email Generation"):
                final_report = st.session_state.agent_response[6].content
        with col5:
            if st.button("Social Media Post"):
                final_report = st.session_state.agent_response[7].content
        st.write(final_report)
    # if st.button("Product Analysis"):
    #     st.write(st.session_state.agent_response[1].content)
    # if st.button("Competitor Analysis"):
    #     st.write(st.session_state.agent_response[4].content)
    # if st.button("Marketing Strategy"):
    #     st.write(st.session_state.agent_response[5].content)
    # if st.button("Email Generation"):
    #     st.write(st.session_state.agent_response[6].content)
    # if st.button("Social Media Post"):
    #     st.write(st.session_state.agent_response[7].content)
# user_input = st.text_input("Give the product :")

# if user_input:
#     agent = build_graph()
#     agent_response = agent.invoke([HumanMessage(content = user_input)])


#     # for message in agent_response:
#     #     st.chat_message("assistant").markdown(message.content)



    # product_analysis_button = st.button("Product Analysis")
    # competitor_analysis_button = st.button("Competitor Analysis")
    # marketing_strategy_button = st.button("Marketing Strategy")
    # email_generation_button = st.button("Email Generation")
    # social_media_post_button = st.button("Social Media Post")

    # if product_analysis_button:
    #     st.write(st.session_state.agent_response[1].content)
    # if competitor_analysis_button:
    #     st.write(st.session_state.agent_response[4].content)
    # if marketing_strategy_button:
    #     st.write(st.session_state.agent_response[5].content)
    # if email_generation_button:
    #     st.write(st.session_state.agent_response[6].content)
    # if social_media_post_button:
    #     st.write(st.session_state.agent_response[7].content)



