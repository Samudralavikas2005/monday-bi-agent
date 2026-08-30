# Monday.com Business Intelligence Agent

An AI-powered Business Intelligence Agent designed for founders and executives to query their Monday.com Deals and Work Orders boards conversationally.

## Features
- **Dynamic API Integration**: Fetches data dynamically from Monday.com boards via GraphQL API v2.
- **Data Resilience**: Built-in data cleaner normalizes messy text, parses dates robustly, and strips currency symbols before processing.
- **Conversational Intelligence**: Powered by open-weights models (via Groq API) and LangChain's Pandas Agent to answer cross-board queries, handle missing data gracefully, and generate executive-level leadership updates.
- **Interactive UI**: A sleek Streamlit interface where users can preview cleaned data and chat with the agent.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Monday.com API Key (Requires read access to boards)
- Groq API Key

### 2. Monday.com Configuration
1. Import the provided `Deal funnel Data.xlsx` and `Work_Order_Tracker Data.xlsx` into Monday.com as **two separate boards**.
2. Note the **Board IDs** for both boards. (You can find the Board ID in the URL of the board: `https://<your_domain>.monday.com/boards/<BOARD_ID>`).
3. Generate a Monday API Token from your Developer section.

### 3. Local Installation
1. Clone or extract this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

### 4. Usage
1. Open the provided local URL (usually `http://localhost:8501`).
2. In the sidebar, input your:
   - Monday.com API Key
   - Groq API Key
   - Deals Board ID
   - Work Orders Board ID
3. Click **Connect & Load Data**.
4. Start chatting with the agent! (e.g., "Give me a leadership update on our pipeline health and highlight any risks.")

## Hosted Prototype
The fully functional prototype is permanently hosted on Render and can be accessed directly here:
**[https://monday-bi-agent-xr43.onrender.com](https://monday-bi-agent-xr43.onrender.com)**

*(Note: The Render free tier spins down after 15 minutes of inactivity. Please allow ~50 seconds for the application to "wake up" upon your first visit if it has been asleep.)*
