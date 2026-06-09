# Directive: Outreach Strategy & Campaign Management

## Goal
Execute high-level, founder-led outbound campaigns that align with the Yono "Reliability" and "Context Layer" messaging.

## Inputs
- Target list (CSV/JSON in `.tmp/`).
- Campaign theme (e.g., "Code & Chaos").
- Founder voice guidelines from `yono_master_context.md`.

## Tools/Scripts
- `execution/generate_outreach_copy.py`: Uses LLM to draft personalized messages based on target LinkedIn/Company data.
- `execution/send_to_crm.py`: Placeholder for pushing data to Google Sheets or CRM.

## Outputs
- Drafted messages in `.tmp/outreach_drafts.json`.
- Campaign log in `.tmp/campaign_summary.md`.

## Instructions
1. Ingest target data from `.tmp/`.
2. Apply the "High-level executive, peer-to-peer" tone.
3. Ensure the word "Deterministic" is NEVER used; use "Reliable."
4. Highlight "Out-of-the-Box Execution" and the "Context Layer."
5. Save drafts for manual review.
