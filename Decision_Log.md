# Decision Log: Monday.com Business Intelligence Agent

## Key Assumptions
1. **API Keys and Authentication**: It is assumed that the user has valid Monday.com and OpenAI API keys. The solution relies on standard Monday GraphQL API (v2) tokens and OpenAI for natural language intelligence.
2. **Board Schema Alignment**: I assumed the user will upload the Excel sheets as boards such that columns roughly match standard concepts (Dates, Revenue/Amount, Status, Sectors). My cleaning pipeline (`data_cleaner.py`) dynamically maps columns by searching for keywords like "date", "cost", "revenue", "status" rather than hardcoding exact column names.
3. **Data Volume**: I assumed the row counts in the Work Orders and Deals boards are small to moderate (a few thousand rows). The current architecture fetches all items into an in-memory Pandas dataframe. This is perfect for BI Agent operations on moderate data but would need pagination/incremental updates for massive datasets.

## Trade-offs Chosen and Why
1. **Pandas + LangChain vs. Direct SQL/GraphQL to Monday.com**: 
   - **Trade-off**: Instead of converting natural language directly to Monday.com GraphQL queries (which is highly complex and error-prone given Monday's nested structure), I chose to extract the data via API into Pandas DataFrames and use LangChain's `create_pandas_dataframe_agent`. 
   - **Why**: This drastically improves query accuracy. Pandas is exceptionally powerful for cross-board operations (merging Deals and Work Orders on common keys), handling missing values (`dropna`, `fillna`), and complex aggregations which Monday's native API does not support out-of-the-box.
2. **Streamlit vs. Full React/Next.js Application**:
   - **Trade-off**: I opted for a Streamlit Python web app rather than a separated React frontend and FastAPI backend.
   - **Why**: Streamlit natively supports interactive chat interfaces (`st.chat_message`) and data visualization components. It allowed me to rapidly prototype a robust, cohesive chat experience where the founder can see their data tables and chat in the same window.

## What I'd Do Differently With More Time
1. **Vector Database / Semantic Search**: I would incorporate a vector database (like Chroma or Pinecone) to perform RAG (Retrieval-Augmented Generation) on text-heavy columns (e.g., meeting notes, project descriptions) to answer qualitative questions ("What are the main reasons deals in the Energy sector are stalling?").
2. **Automated Visualization**: Right now, the agent returns text-based Markdown answers. With more time, I would have the agent generate dynamic Altair or Plotly charts based on the query, injecting them directly into the Streamlit chat stream.
3. **Webhooks for Real-Time Sync**: Instead of fetching the entire board on demand, I would set up Monday.com webhooks to listen for item creations/updates and sync them into a persistent SQL database (e.g., PostgreSQL). This would make the app instantly scalable.

## Interpretation of "Leadership Updates"
**Interpretation**: "Leadership updates" refers to highly structured, executive-level summaries that prioritize bottom-line metrics over granular data points. A founder doesn't just want a list of deals; they want to know the *health* of the business. 

**Implementation**: I instructed the LangChain LLM system prompt specifically on this point. When the agent detects a request for an update or summary, it structures its response into:
1. **Executive Summary** (High-level health)
2. **Key Metrics** (Aggregated numbers: Total Pipeline, Blocked Work Orders)
3. **Risks/Caveats** (Explicitly pointing out missing data, such as "15% of deals lack a specified sector")
This transforms the agent from a simple data-fetcher into a strategic assistant.
