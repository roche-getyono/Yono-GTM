# Directive: VC Narrative & Strategy

## Goal
To maintain a high-context, consistent narrative for the Yono V2 Seed round, focusing on technical reliability and infrastructure-first AI.

## The Narrative: "The Anti-Hype"
The core narrative for this fundraise is that Yono is the solution to the **AI Hallucination & Engineering Distraction** problem.

### Key Messaging
1. **Infrastructure, not Apps:** We don't build the UI; we build the engine that makes the UI reliable.
2. **Code as Truth:** By reverse-engineering the frontend repo, we bypass the need for probabilistic LLM wrappers.
3. **Speed to Market:** Deploy natural language execution overnight, without pulling the backend team off the core roadmap.

## Outreach Workflow
1. **Identify Targets:** Use `scripts/search_investors.py` to find VCs with heavy B2B SaaS portfolios.
2. **Persona Research:** Create/Update profiles in `personas/` (e.g., `kobi_persona.md`).
3. **Draft Outreach:** Use `execution/generate_outbound_messages.py` with the `context/vc_forwardable_template.md`.
4. **Track Status:** Update `context/investor_status.txt` and `context/investor_tracking.xlsx`.

## Assets
- `context/yono_master_context.md`: Deep technical background.
- `context/vc_forwardable_template.md`: The standard "hook" for warm introductions.
