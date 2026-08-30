import streamlit as st
import pandas as pd
from monday_api import MondayClient
from data_cleaner import DataCleaner
from agent import BIAgent

st.set_page_config(page_title="Monday.com BI Agent", page_icon="📊", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")
st.markdown("""
Welcome to the AI-powered Business Intelligence Agent for Monday.com. 
This agent helps founders and executives get quick, accurate answers to business questions across Work Orders and Deals boards.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    monday_api_key = st.text_input("Monday.com API Key", type="password")
    openai_api_key = st.text_input("Groq API Key (Free)", type="password")
    deals_board_id = st.text_input("Deals Board ID")
    work_orders_board_id = st.text_input("Work Orders Board ID")
    
    available_models = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]
    selected_model = st.selectbox("Groq Model", available_models, index=0)
    
    load_data_btn = st.button("Connect & Load Data")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your BI Agent. Ask me anything about your Deals or Work Orders data."}]
if "deals_df" not in st.session_state:
    st.session_state.deals_df = None
if "work_orders_df" not in st.session_state:
    st.session_state.work_orders_df = None
if "agent_initialized" not in st.session_state:
    st.session_state.agent_initialized = False

# Load Data logic
if load_data_btn:
    if not (monday_api_key and openai_api_key and deals_board_id and work_orders_board_id):
        st.error("Please provide all API keys and Board IDs in the sidebar.")
    else:
        with st.spinner("Fetching data from Monday.com..."):
            try:
                monday_client = MondayClient(api_key=monday_api_key)
                
                # Fetch Deals
                raw_deals = monday_client.fetch_board_data(deals_board_id)
                st.session_state.deals_df = DataCleaner.clean_deals_data(raw_deals)
                
                # Fetch Work Orders
                raw_work_orders = monday_client.fetch_board_data(work_orders_board_id)
                st.session_state.work_orders_df = DataCleaner.clean_work_orders_data(raw_work_orders)
                
                # Initialize Agent
                st.session_state.bi_agent = BIAgent(
                    deals_df=st.session_state.deals_df,
                    work_orders_df=st.session_state.work_orders_df,
                    openai_api_key=openai_api_key,
                    model_name=selected_model
                )
                
                st.session_state.agent_initialized = True
                st.success("Successfully connected to Monday.com and loaded data!")
                
                with st.expander("Preview Deals Data (Cleaned)"):
                    st.dataframe(st.session_state.deals_df.head())
                with st.expander("Preview Work Orders Data (Cleaned)"):
                    st.dataframe(st.session_state.work_orders_df.head())
                    
            except Exception as e:
                st.error(f"Error connecting to Monday.com: {e}")

# Chat Interface
if st.session_state.agent_initialized:
    st.divider()
    st.subheader("💬 Chat with your Data")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask a question (e.g., 'How is our pipeline looking for the energy sector?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = st.session_state.bi_agent.query(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please configure your API keys and Board IDs in the sidebar, then click 'Connect & Load Data' to start chatting.")
