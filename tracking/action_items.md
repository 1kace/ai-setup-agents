# Action Items

This file tracks pending tasks and issues for the AI Setup Agents project and related environment configurations.

## Open Items

-   **[ ] Migrate C:\SYSDIR Contents:** Instruct user to move the contents of the legacy `C:\SYSDIR` directory to the new standard location (`%USERPROFILE%\Documents\SYSDIR`) on the Windows machine at an appropriate time.
    -   *Status:* Pending - Requires user action.
    -   *Next Step:* Provide instructions to the user when system configuration tasks involving `SYSDIR` are being performed.
-   **[ ] Remove Empty C:\SYSDIR:** After confirming contents have been migrated, instruct user to remove the now-empty legacy `C:\SYSDIR` directory.
    -   *Status:* Pending - Depends on migration completion.
    -   *Next Step:* Provide instructions after the migration action item is completed.
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
