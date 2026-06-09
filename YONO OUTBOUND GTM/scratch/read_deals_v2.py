import pandas as pd
import os

file_path = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\Deals_1777136186.xlsx'

try:
    # Row 4 (1-indexed) is the header, so header=4 in pandas (which is 0-indexed)
    df = pd.read_excel(file_path, header=4)
    print("Columns:", df.columns.tolist())
    
    # Filter out rows where 'Name' is NaN
    df = df.dropna(subset=['Name'])
    
    # Select relevant columns
    relevant_cols = ['Name', 'Seed Round Stage', 'Status', 'Contacts']
    df_clean = df[relevant_cols]
    
    print("\nInvestor Deals:\n", df_clean.to_string())
except Exception as e:
    print(f"Error: {e}")
