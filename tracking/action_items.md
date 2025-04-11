# Action Items

This file tracks pending tasks and issues for the AI Setup Agents project and related environment configurations.

## Open Items

-   **[X] Migrate C:\SYSDIR Contents:** User moved contents of the legacy `C:\SYSDIR` directory to `C:\Users\mhadmin\Documents\ABRIDER`.
    -   *Status:* Completed (User performed action 2025-04-10).
-   **[ ] Remove Empty C:\SYSDIR:** After confirming contents have been migrated, instruct user to remove the now-empty legacy `C:\SYSDIR` directory.
    -   *Status:* Ready - Migration complete.
    -   *Next Step:* Instruct user to verify `C:\SYSDIR` is empty and then remove it (e.g., using `rmdir C:\SYSDIR` in an admin prompt).
-   **[ ] Secure ABRIDER Folder Permissions:** Investigate and apply appropriate permissions to the `C:\Users\mhadmin\Documents\ABRIDER` folder to restrict access (e.g., only to `mhadmin` and `Administrators`).
    -   *Status:* Pending - New requirement based on user feedback.
    -   *Next Step:* Research and provide `icacls` or PowerShell commands to set desired permissions.
-   **[ ] Install ansible-lint on ssca02echob:** Install `ansible-lint` in the Python virtual environment within the project directory on the `ssca02echob` Ubuntu sandbox.
    -   *Status:* Pending - Deferred until Knowledge Management (KM) / P&P structure is finalized and implemented. Requires connecting VS Code to the `ssca02echob` SSH session with the project folder opened as a workspace.
    -   *Next Step:* Execute installation steps outlined in previous task context once KM setup is complete and the correct VS Code environment is active.
-   **[ ] Design KMAgent & KBPA:** Design and plan the implementation of the Knowledge Management Agent (KMAgent) and the KB Processor Agent (KBPA) responsible for processing LLM artifacts and integrating insights into the project KB.
    -   *Status:* Pending - Concept defined in `kb/README.md`.
    -   *Next Step:* Further discussion and architectural planning required. Define specific inputs, outputs, processing logic, and integration points.
-   **[ ] Plan Permission Delegation:** Plan for future delegation of permissions currently held by Cline ("Superuser") to more specialized agents, particularly when considering execution environments beyond the user's local VS Code.
    -   *Status:* Pending - Concept noted in `kb/README.md`.
    -   *Next Step:* Define specific permissions, target agents, and triggers/conditions for delegation as the system architecture matures.
-   **[ ] Investigate EB Session Completion:** Diagnose why the Cline instance running in the remote SSH (EB/`ssca02echob`) session sometimes fails to complete its full sequence of commands/reporting, especially after script execution or errors.
    -   *Status:* Pending - Observed multiple times during `ansible-lint` / `qa_agent.py` testing.
    -   *Next Step:* Monitor future EB session tasks. If it persists, consider simplifying command chains, checking SSH extension logs/behavior, or adding more robust error handling within agent scripts run remotely.
-   **[ ] Investigate Ansible Locale Issue on ssca02echob:** Determine the root cause of the persistent "unsupported locale setting" error encountered by Ansible tools (`ansible-lint`, `ansible-config`) on `ssca02echob`, even after system locale generation and explicit environment variable setting.
    -   *Status:* **Deferred** - Standard fixes were ineffective. `qa_agent.py` now bypasses the error. `ansible-lint` integration is currently non-functional on `ssca02echob`.
    -   *Next Step:* Revisit if deploying to a different environment or if deeper system investigation on `ssca02echob` becomes feasible. Current focus shifted to enhancing the custom rules engine of `QAAgent`.
-   **[ ] Deploy & Test `qa_agent.py` v1.1 (Refined Parsing):** The latest version of `qa_agent.py` (with refined ansible-lint parsing) needs to be pushed to `origin/master` and then tested on `ssca02echob`.
    -   *Status:* **Blocked** - Pending resolution of Git push/pull issues or reliable Git integration for Cline.
    -   *Next Step:* Once Git push is confirmed working (either manually or via new integration), instruct EB to `git pull origin master` and run the final verification test.
-   **[ ] Implement Reliable Git Integration for Cline:** Investigate and implement a method for Cline to reliably perform Git operations (add, commit, pull, push) without requiring manual user intervention for every step.
    -   *Status:* Pending - Current custom MCP server lacks necessary tools (`git_pull`), and manual process is unreliable/undesirable.
    -   *Next Step:* Evaluate options:
        -   Enhance the custom `github-mcp-server` to include `git_pull` and potentially conflict resolution logic (complex).
        -   Install and configure a VS Code extension like `vscode-as-mcp-server` (as researched in `kb/mcp/vscode_github_integration.md`) to expose Git tools via MCP.
        -   Explore other potential solutions (e.g., dedicated Git CLI tools accessible via `execute_command` if authentication can be handled non-interactively).

## Recommended Next Steps

-   Focus on designing the KMAgent & KBPA (see open item above).
-   Address securing the `ABRIDER` folder permissions.
-   Instruct user to remove the empty `C:\SYSDIR`.
