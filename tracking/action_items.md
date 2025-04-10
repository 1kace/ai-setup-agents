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
