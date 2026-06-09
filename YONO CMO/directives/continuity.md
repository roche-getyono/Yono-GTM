# System Directive: Context Continuity

This directive ensures that the agent maintains a consistent understanding of the workspace history, even if the UI history is unavailable.

## Protocol

1.  **Always Check the Log**: Upon initialization in this workspace, the agent MUST check for the presence of `CONVERSATION_LOG.md` in the root directory.
2.  **Reference Previous Context**: If the user mentions a topic documented in the log, the agent should use the associated Conversation ID to retrieve relevant context from the `brain` directory.
3.  **Update the Log**: At the end of every significant task or at the conclusion of a session, the agent MUST update `CONVERSATION_LOG.md` with the current session ID and a brief summary of what was accomplished.
4.  **Path Awareness (CRITICAL)**: The primary workspace is now at `c:\Users\danie\Desktop\YONO CMO`. You MUST avoid opening files from the old `OneDrive` path, as this causes history loss in the Agent Manager.
5.  **Manual Source of Truth**: If the sidebar history is empty, refer to `CONVERSATION_LOG.md` to bridge the context gap.
