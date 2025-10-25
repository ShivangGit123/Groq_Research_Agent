import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper , ArxivAPIWrapper 
from langchain_community.tools import ArxivQueryRun , WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent , AgentType
import os
from dotenv import load_dotenv
from langchain_community.callbacks import StreamlitCallbackHandler

ArxivAPIWrapper = ArxivAPIWrapper(top_k_results = 1 , doc_content_chars_max=1200) 
arxiv = ArxivQueryRun(api_wrapper= ArxivAPIWrapper)

WikipediaAPIWrapper=WikipediaAPIWrapper(top_k_results=1 , doc_content_chars_max=1200) 
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper)

search  = DuckDuckGoSearchRun(name = "Search")


st.title("🔎 Groq Research Agent")
api_key = st.sidebar.text_input("Groq API Key", type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role" :"assistant" , "content" : "Hi, I am a research assistant who can use Arxiv, Wikipedia, and web search. How can I assist you with a detailed explanation?"
    }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])    


if prompt:=st.chat_input(placeholder="What is Machine Learning?"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
        st.stop()
        
    st.session_state.messages.append({"role":"user" , "content":prompt})
    st.chat_message("user").write(prompt)

    system_prompt = (
        "You are an expert, highly verbose AI assistant specialized in research. "
        "Your primary goal is to provide **detailed, exhaustive, and educational explanations**. "
        "Every answer must be clearly structured, use formal academic tone, and include multiple, well-developed paragraphs. "
        "You must elaborate on every point and provide necessary context. "
        "**Crucially, every final response must be at least 200 words long.** Always provide a comprehensive and thorough answer. "
        "Avoid short, superficial, or single-paragraph responses at all costs."
    )

    llm = ChatGroq(model_name="llama-3.1-8b-instant" , api_key=api_key , streaming=True)
    tools = [arxiv , wiki , search]

    search_agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        handling_parsing_errors=True, 
        agent_kwargs={ 
            "system_message": system_prompt
        }
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container() ,expand_new_thoughts=False)
        try:
            response = search_agent.invoke({"input" : prompt}, {"callbacks":[st_cb]})['output']
            st.session_state.messages.append({'role':'assistant' , "content":response})
        except Exception as e:
            error_message = f"An error occurred: {e}. Please check your API key and ensure the prompt is clear."
            st.error(error_message)
            st.session_state.messages.append({'role':'assistant' , "content":error_message})
