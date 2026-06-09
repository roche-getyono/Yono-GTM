import pandas as pd
import json
import re

def test():
    with open('2_config/icp_filters.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    exclude_company_keywords = [e.lower() for e in config.get('exclude_company_keywords', [])]
    
    company = "Macquarie Group".lower()
    
    for kw in exclude_company_keywords:
        if kw in company:
            print(f"MATCH: {kw} in {company}")
            return
    print("NO MATCH")

if __name__ == "__main__":
    test()
