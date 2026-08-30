import os
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

class BIAgent:
    def __init__(self, deals_df: pd.DataFrame, work_orders_df: pd.DataFrame, openai_api_key: str = None):
        self.deals_df = deals_df
        self.work_orders_df = work_orders_df
        api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("Groq API key must be provided")
            
        self.llm = ChatGroq(
            temperature=0, 
            model_name="mixtral-8x7b-32768",
            groq_api_key=api_key
        )
        
        self.agent = create_pandas_dataframe_agent(
            self.llm,
            [self.deals_df, self.work_orders_df],
            verbose=True,
            agent_type="openai-tools",
            allow_dangerous_code=True,
            prefix="""You are an expert Business Intelligence AI Agent working for the founders and leadership team of a company.
Your goal is to answer founder-level business queries about revenue, pipeline health, sectoral performance, and operational metrics.

You have access to two pandas DataFrames:
- df1: Deals (Sales pipeline data)
- df2: Work Orders (Project execution data)

Core Responsibilities:
1. Data Resilience: Handle missing/null values, NaNs, and inconsistent formats gracefully before performing calculations.
2. Cross-Board Querying: Query across both DataFrames when needed (using merges/joins on common keys like Project IDs or Names).
3. Business Intelligence: Provide strategic context, insights, and synthesized analysis, not just raw numbers. 
4. Leadership Updates: If asked to prepare leadership updates, structure your response professionally (Executive Summary, Key Metrics, Risks/Caveats).

Important Guidelines:
- If a query is vague, state your assumptions clearly before answering.
- ALWAYS communicate data quality issues or caveats to the user (e.g., "Note: 15% of the deals lack a specified sector").
- Format the final output clearly using Markdown (bullet points, bold text).
"""
        )

    def query(self, user_question: str) -> str:
        try:
            response = self.agent.invoke({"input": user_question})
            return response.get("output", "I could not generate an answer.")
        except Exception as e:
            return f"An error occurred while analyzing the data: {str(e)}"
