import os
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
import time

MONDAY_API_URL = "https://api.monday.com/v2"

class MondayClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("MONDAY_API_KEY")
        if not self.api_key:
            raise ValueError("Monday API key must be provided")
        self.headers = {
            "Authorization": self.api_key,
            "API-Version": "2024-01"
        }

    def fetch_board_data(self, board_id: str) -> pd.DataFrame:
        """Fetches all items from a given Monday.com board and returns as a DataFrame."""
        items = []
        has_next_page = True
        cursor = None
        
        while has_next_page:
            query = self._build_query(board_id, cursor)
            response = requests.post(MONDAY_API_URL, json={"query": query}, headers=self.headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data from Monday.com: {response.text}")
                
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
                
            try:
                board_data = data["data"]["boards"][0]
                items_page = board_data["items_page"]
                fetched_items = items_page["items"]
                cursor = items_page.get("cursor")
                
                for item in fetched_items:
                    parsed_item = {"Item ID": item["id"], "Item Name": item["name"]}
                    for col in item.get("column_values", []):
                        col_title = col["column"]["title"] if col.get("column") else col["id"]
                        parsed_item[col_title] = col.get("text", "")
                    items.append(parsed_item)
                    
                if not cursor:
                    has_next_page = False
                    
            except (KeyError, IndexError) as e:
                raise Exception(f"Unexpected response structure from Monday API: {e}")
                
            time.sleep(0.1) # Rate limiting protection
            
        return pd.DataFrame(items)

    def _build_query(self, board_id: str, cursor: Optional[str] = None) -> str:
        cursor_arg = f', cursor: "{cursor}"' if cursor else ""
        return f"""
        query {{
            boards(ids: [{board_id}]) {{
                items_page(limit: 100{cursor_arg}) {{
                    cursor
                    items {{
                        id
                        name
                        column_values {{
                            id
                            text
                            type
                            value
                            column {{
                                title
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
