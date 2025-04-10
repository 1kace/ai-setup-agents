# Procedure: Initial Device Setup (Standardized)

This procedure outlines the standard steps for setting up a new device environment (e.g., a remote SSH host) for the `ai-setup-agents` project, adhering to company policies.

**Assumptions:**
*   The target device is a Linux-based system.
*   The designated operational user is `abriderc`.
*   `sudo` privileges are available for initial directory creation and ownership changes.
*   The standard base directory is `/opt/<HOSTNAME>` (e.g., `/opt/SSCA02ECHOB`).

**Steps:**

1.  **Create Base SYSDIR & Set Ownership:**
    *   Command: `sudo mkdir -p /opt/<HOSTNAME> && sudo chown abriderc:abriderc /opt/<HOSTNAME>`
    *   Purpose: Creates the standard base directory and assigns ownership to the `abriderc` user. Replace `<HOSTNAME>` with the actual hostname (e.g., `SSCA02ECHOB`).

2.  **Create Project Directory & Set Ownership:**
    *   Command: `sudo mkdir -p /opt/<HOSTNAME>/repos/ai-setup-agents && sudo chown abriderc:abriderc /opt/<HOSTNAME>/repos/ai-setup-agents`
    *   Purpose: Creates the specific project directory within the base and assigns ownership.

3.  **Open Workspace in VS Code:**
    *   Action: Instruct the user to open `/opt/<HOSTNAME>/repos/ai-setup-agents` as the workspace in VS Code (`File > Open Folder...`).
    *   Emphasis: Wait for the workspace to fully load before proceeding.

4.  **Clone Repository:**
    *   Context: Run within the VS Code integrated terminal (connected to the remote host, running as `abriderc`, in the workspace directory).
    *   Command: `git clone https://github.com/1kace/ai-setup-agents .`
    *   Purpose: Clones the repository content into the current workspace directory.

5.  **Set Repository Permissions:**
    *   Context: Run within the VS Code integrated terminal.
    *   Command: `chmod 700 /opt/<HOSTNAME>/repos/ai-setup-agents`
    *   Purpose: Restricts access (read/write/execute) to the repository directory to only the owner (`abriderc`).
