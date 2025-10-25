import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper , ArxivAPIWrapper 
from langchain_community.tools import ArxivQueryRun , WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub 
from langchain_core.prompts import PromptTemplate 
from langchain_community.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv


ArxivAPIWrapper = ArxivAPIWrapper(top_k_results = 1 , doc_content_chars_max=1200) 
arxiv = ArxivQueryRun(api_wrapper= ArxivAPIWrapper)

WikipediaAPIWrapper=WikipediaAPIWrapper(top_k_results=1 , doc_content_chars_max=1200) 
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper)

search = DuckDuckGoSearchRun(name = "Search")


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

    SYSTEM_INSTRUCTIONS = (
        "You are an expert, highly verbose AI assistant specialized in research. "
        "Your primary goal is to provide **detailed, exhaustive, and educational explanations**. "
        "Every answer must be clearly structured, use formal academic tone, and include multiple, well-developed paragraphs. "
        "You must elaborate on every point and provide necessary context. "
        "**Crucially, every final response must be at least 200 words long.** Always provide a comprehensive and thorough answer. "
        "Avoid short, superficial, or single-paragraph responses at all costs."
    )

    prompt_template = hub.pull("hwchase17/react") 
    
    llm = ChatGroq(model_name="gemma2-9b-it" , api_key=api_key , streaming=True)
    tools = [arxiv , wiki , search]

    custom_prompt = prompt_template.partial(
        agent_scratchpad="",
        input="",
        tool_names=", ".join([t.name for t in tools]) 
    ).partial(
        instructions=SYSTEM_INSTRUCTIONS
    )

    agent_runnable = create_react_agent(
        llm, 
        tools, 
        custom_prompt 
    )
    
    search_agent_executor = AgentExecutor(
        agent=agent_runnable, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container() ,expand_new_thoughts=False)
        
        try:
            response = search_agent_executor.invoke({"input" : prompt}, {"callbacks":[st_cb]})['output']
            st.session_state.messages.append({'role':'assistant' , "content":response})
        except Exception as e:
            error_message = f"An error occurred: {e}. Please check your API key and ensure the prompt is clear."
            st.error(error_message)
            st.session_state.messages.append({'role':'assistant' , "content":error_message})
