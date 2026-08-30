import pandas as pd
import numpy as np
import re
from datetime import datetime

class DataCleaner:
    @staticmethod
    def clean_deals_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        df = df.copy()
        
        # Standardize column names
        df.columns = [DataCleaner._normalize_column_name(col) for col in df.columns]
        
        # Try to identify and clean date columns
        date_cols = [col for col in df.columns if 'date' in col or col in ['created_at', 'updated_at', 'closed_at']]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        # Clean currency/numeric columns (e.g. Value, Amount)
        money_cols = [col for col in df.columns if any(x in col for x in ['amount', 'value', 'revenue', 'cost', 'price'])]
        for col in money_cols:
            if col in df.columns and df[col].dtype == 'object':
                # Remove currency symbols and commas
                df[col] = df[col].astype(str).str.replace(r'[$,£€]', '', regex=True)
                df[col] = df[col].str.replace(',', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # Standardize text/categorical columns (e.g. Status, Stage, Sector)
        cat_cols = [col for col in df.columns if any(x in col for x in ['status', 'stage', 'sector', 'industry', 'priority'])]
        for col in cat_cols:
            if col in df.columns and df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.title()
                df[col] = df[col].replace('Nan', np.nan)
                
        # Handle nulls
        # We don't want to drop them as they might be important missing data, 
        # so we leave NaNs which pandas/LLM can handle gracefully.
        
        return df

    @staticmethod
    def clean_work_orders_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        df = df.copy()
        
        # Standardize column names
        df.columns = [DataCleaner._normalize_column_name(col) for col in df.columns]
        
        # Try to identify and clean date columns
        date_cols = [col for col in df.columns if 'date' in col or 'time' in col]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        # Clean numeric metrics
        numeric_cols = [col for col in df.columns if 'hours' in col or 'cost' in col or 'qty' in col or 'quantity' in col]
        for col in numeric_cols:
            if col in df.columns and df[col].dtype == 'object':
                # Extract numbers
                df[col] = df[col].astype(str).str.extract(r'([\d.]+)')[0]
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # Standardize categorical columns
        cat_cols = [col for col in df.columns if 'status' in col or 'priority' in col or 'type' in col]
        for col in cat_cols:
            if col in df.columns and df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.title()
                df[col] = df[col].replace('Nan', np.nan)
                
        return df

    @staticmethod
    def _normalize_column_name(name: str) -> str:
        # Lowercase, replace spaces with underscores, remove special characters
        if pd.isna(name):
            return "unnamed"
        name = str(name).strip().lower()
        name = re.sub(r'[^a-z0-9_]', '_', name)
        name = re.sub(r'_+', '_', name) # Replace multiple underscores with single
        name = name.strip('_')
        return name
