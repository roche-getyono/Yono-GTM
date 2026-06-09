# Directive: Triage and Categorize Contacts

## Goal
Process Daniel's raw LinkedIn connections to separate high-value SaaS Design Partners from VC/Investor connections, while aggressively filtering out noise.

## Inputs
- `1_input/Connections.csv`: Raw LinkedIn export.
- `2_config/icp_filters.json`: The rules engine for categorization.

## Process
Write a Python script using pandas to process the CSV row by row using this exact logic flow:

1. **Clean:** Drop any row where 'Company' or 'Position' is blank.
2. **The "Trash" Filter:** If the 'Company' contains any word from `exclude_company_keywords`, OR the 'Position' contains any word from `exclude_title_keywords`, drop the row entirely.
3. **The "VC" Bucket:** If the 'Company' or 'Position' contains any word from `vc_keywords`, label this row's 'Category' as `VC / Investor`.
4. **The "Target" Bucket:** If the row is not a VC, AND the 'Position' exactly matches or contains a string from `target_titles`, label this row's 'Category' as `SaaS Target`.
5. **Discard:** If a row does not fit into the VC or Target buckets, drop it.

## Outputs
Save the final DataFrame into two separate files:
1. `/3_output/Phase1_Warm_Targets.csv` (Only rows categorized as 'SaaS Target')
2. `/3_output/VC_Network.csv` (Only rows categorized as 'VC / Investor')