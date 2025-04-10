# Common Knowledge Base

This directory contains general policies, procedures, and knowledge applicable across multiple agents or roles within the AI Setup Agents project.

## Core Operational Procedures

1.  **Environment Verification:** Before executing commands or modifying files, **verify the current execution environment and VS Code workspace connection.** Ensure you are operating in the intended context (e.g., local Windows, specific remote SSH host like `ssca02echob`) and that the correct project folder is open as the workspace. If generating context for a new task that requires a different environment, explicitly state the target environment and the need to switch VS Code context.
2.  **Confirmation for Destructive Actions:** Before performing potentially destructive actions (e.g., deleting files or directories using `rm`, overwriting files with `write_to_file` if unsure of impact, modifying critical configuration), explicitly state the intended action and request user confirmation using `ask_followup_question`. Copy operations (`cp`) are generally safer than move (`mv`) or delete (`rm`).
3.  **Context Handoff & Referencing:**
    *   **For large context blocks** (e.g., task handoffs, detailed plans): Write the context to a temporary file within the project's `.tmp/` directory (e.g., `.tmp/task_handoff_YYYYMMDD_HHMMSS.md`). Instruct the user to provide this file path as context in the new session/task. Ensure `.tmp/` is in `.gitignore`.
    *   **For smaller references:** Briefly summarize or quote the relevant part of the previous message. Avoid re-providing large blocks directly in chat to conserve tokens.
4.  **Pre-Context Switch Sync:** Before switching development context (e.g., from local Windows to remote SSH `ssca02echob`, or vice-versa), ensure all intended changes in the **current** context have been committed and pushed to the central GitHub repository (`origin/master`). This prevents merge conflicts and ensures the next session starts with the latest consistent state. Verify the push was successful before proceeding with the context switch.

Referenced files:
*   `c:/SYSDIR/ASA/kb/common/README.md` (for sensitive/environment-specific common knowledge - path may change to ABRIDER)
