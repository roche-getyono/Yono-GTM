import pandas as pd
import os

file_path = r'c:\Users\danie\OneDrive\Desktop\YONO OUTBOUND GTM\Deals_1777136186.xlsx'

try:
    df = pd.read_excel(file_path)
    print(df.to_string())
except Exception as e:
    print(f"Error: {e}")
