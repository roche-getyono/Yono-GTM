import pandas as pd
import json
import os
import io
import re

def filter_contacts():
    # Paths
    config_path = os.path.join('2_config', 'icp_filters.json')
    input_path = os.path.join('1_input', 'Connections.csv')
    output_targets = os.path.join('3_output', 'Phase1_Warm_Targets.csv')
    output_vc = os.path.join('3_output', 'VC_Network.csv')

    # Load config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    target_titles = [t.lower() for t in config.get('target_titles', [])]
    vc_keywords = [k.lower() for k in config.get('vc_keywords', [])]
    exclude_company_keywords = [e.lower() for e in config.get('exclude_company_keywords', [])]
    exclude_title_keywords = [e.lower() for e in config.get('exclude_title_keywords', [])]
    known_vc_companies = [c.lower() for c in config.get('known_vc_companies', [])]
    known_saas_companies = [c.lower() for c in config.get('known_saas_companies', [])]
    
    gtm_keywords = [k.lower() for k in config.get('gtm_keywords', [])]
    product_eng_keywords = [k.lower() for k in config.get('product_eng_keywords', [])]
    enterprise_tech_companies = [c.lower() for c in config.get('enterprise_tech_companies', [])]
    
    relevant_role_keywords = gtm_keywords + product_eng_keywords

    # Read CSV, skipping preamble
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(input_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()

    csv_start = 0
    for i, line in enumerate(lines):
        if 'First Name,' in line:
            csv_start = i
            break
            
    csv_data = "".join(lines[csv_start:])
    df = pd.read_csv(io.StringIO(csv_data))

    # 1. Clean: Drop any row where 'Company' or 'Position' is blank.
    df = df.dropna(subset=['Company', 'Position'])

    def get_category_and_reason(row):
        company = str(row['Company']).lower()
        position = str(row['Position']).lower()

        # --- 1. Trash Filter (Global Exclusions) ---
        for kw in exclude_company_keywords:
            if kw in company:
                return 'Drop', f'Excluded Company Keyword: {kw}'
        for kw in exclude_title_keywords:
            if kw in position:
                return 'Drop', f'Excluded Title Keyword: {kw}'

        # --- 2. VC / Investor Triage (Stricter) ---
        # A) Known VC check (Highest Priority)
        for vc_co in known_vc_companies:
            if vc_co in company:
                return 'VC / Investor', f'Known VC Company: {vc_co}'
        
        # B) Investor Title + Venture Company Pattern
        # Titles often found in VCs
        investor_titles = ['partner', 'principal', 'associate', 'analyst', 'investor', 'venture', 'investment', 'managing director', 'scout']
        # Keywords indicating a Venture/Investment firm
        venture_cos = ['ventures', 'capital', 'partners', 'fund', 'equity', 'angel', 'syndicate']
        
        has_investor_title = any(re.search(rf'\b{re.escape(t)}\b', position) for t in investor_titles)
        has_venture_co = any(re.search(rf'\b{re.escape(c)}\b', company) for c in venture_cos)
        
        # Additional Exclusions for VCs (to avoid Law, HR, etc.)
        vc_exclusions = ['success', 'people', 'talent', 'hr', 'hiring', 'recruitment', 'legal', 'law', 'accounting', 'marketing services', 'business partner', 'project manager', 'channel partner']
        has_vc_exclusion = any(kw in position for kw in vc_exclusions) or any(kw in company for kw in vc_exclusions)
        
        if has_investor_title and has_venture_co and not has_vc_exclusion:
            return 'VC / Investor', 'Investor Title + Venture Company Pattern'

        # C) Catch-all for very specific VC titles (e.g., "General Partner" anywhere)
        specific_vc_titles = ['general partner', 'managing partner', 'venture partner', 'investor relations']
        for t in specific_vc_titles:
            if t in position and not has_vc_exclusion:
                return 'VC / Investor', f'Specific VC Title: {t}'

        # --- 3. SaaS Target Triage ---
        
        # Known SaaS check
        for saas_co in known_saas_companies:
            if saas_co in company:
                return 'SaaS Target', f'Known SaaS Company: {saas_co}'

        # Helper to check for relevant roles (with word boundaries)
        def has_relevant_role(pos):
            for kw in relevant_role_keywords:
                if re.search(rf'\b{re.escape(kw)}\b', pos):
                    return True
            return False

        # a) Enterprise Tech Logic (Wix, monday, etc.)
        is_enterprise_tech = any(ent in company for ent in enterprise_tech_companies)
        if is_enterprise_tech:
            if not has_relevant_role(position):
                return 'Drop', 'Enterprise Tech: Non-GTM/Prod/Eng role'

        # b) Founder Title Logic
        founder_keywords = ['founder', 'co-founder', 'ceo', 'cpo', 'cto', 'chief executive officer', 'chief product officer']
        is_founder = any(re.search(rf'\b{re.escape(kw)}\b', position) for kw in founder_keywords)
        if is_founder:
            return 'SaaS Target', 'Found High-Value Title (Founder/C-Suite)'

        # c) Director Title Logic
        if re.search(rf'\bdirector\b', position):
            if has_relevant_role(position):
                return 'SaaS Target', 'Target Title Match: Director with relevant role'
            else:
                return 'Drop', 'Director without relevant role'

        # d) Remaining Target Titles (VP, etc.)
        for kw in target_titles:
            kw_lower = kw.lower()
            if kw_lower in founder_keywords or kw_lower == 'director':
                continue
            if re.search(rf'\b{re.escape(kw_lower)}\b', position):
                return 'SaaS Target', f'Target Title Match: {kw}'

        return 'Drop', 'No Match'

    # Apply categorization
    results = df.apply(get_category_and_reason, axis=1)
    df['Category'] = [r[0] for r in results]
    df['Match_Reason'] = [r[1] for r in results]

    # Filter into buckets
    df_targets = df[df['Category'] == 'SaaS Target']
    df_vcs = df[df['Category'] == 'VC / Investor']

    # Write output
    os.makedirs(os.path.dirname(output_targets), exist_ok=True)
    df_targets.to_csv(output_targets, index=False)
    df_vcs.to_csv(output_vc, index=False)

    print(f"Total VC rows: {len(df_vcs)}")
    print(f"Total Target rows: {len(df_targets)}")

if __name__ == "__main__":
    filter_contacts()
