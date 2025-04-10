# Project Knowledge Base

This directory serves as the central knowledge base for the AI Setup Agents (ASA) project.

## Project Overview

The AI Setup Agents project aims to create a multi-agent system to assist with system configuration, setup, and quality assurance tasks.

## Repository Information

*   **GitHub URL:** https://github.com/1kace/ai-setup-agents/

## Agent Roles and Interactions

*   **Cline (ASA Architect & Orchestrator):** The primary interface for interacting with the ASA system. Responsible for:
    *   Architecting the overall system design.
    *   Orchestrating tasks between different agents (both internal ASA agents and external interfaces like GWA).
    *   Implementing core components and policies.
    *   Maintaining the project's knowledge base and action items.
    *   **Current Status:** Considered "Superuser" with full permissions within the current development environment (VS Code on user's workstation).
    *   **Future State:** Permissions may be delegated to more specialized agents as the system evolves and potentially moves to a different execution environment.
*   **Gemini Web ASA Agent (GWA):** Refers to the interactions and prompts used within the Gemini Web UI prior to or alongside Cline's involvement. Serves as:
    *   The initial source for sketching out project concepts and requirements.
    *   A potential source for specific task instructions or context, which Cline will adapt and integrate according to established project P&Ps.
    *   **Interaction Flow:** When a task originates from GWA, Cline will perform the necessary actions and, upon completion, provide a summary message intended for the user to relay back to GWA to keep its context synchronized.
    *   The role and interaction model with GWA will be refined as the project progresses.
*   **Internal ASA Agents (e.g., ConfigAgent, QAAgent, ArchAgent):** Specialized agents within the `src/agents/` directory designed to handle specific functions like configuration application, quality assurance checks, and architectural analysis/generation. Cline orchestrates the use of these agents.
*   **Knowledge Management Agent (KMAgent) (Proposed):** Future agent responsible for overseeing the project's knowledge base, potentially managing the KBPA.
*   **KB Processor Agent (KBPA) (Proposed):** Future agent specialized in processing artifacts (e.g., conversation logs, prompts) from various LLM UIs (GWA, Claude, ChatGPT, etc.) to identify and integrate valuable concepts or requirements into the structured project KB. May utilize common and task-specific embeddings.

## GWA Interaction Procedure

1.  User provides Cline with a prompt/task originating from GWA.
2.  Cline **verifies** the GWA prompt against the current project state, established plans, and P&Ps.
    *   If the GWA prompt conflicts with established context or procedures (e.g., incorrect environment assumption, conflicting goals), Cline will **notify the user** of the discrepancy and recommend a course of action (e.g., correcting GWA's context, rejecting the conflicting instruction).
    *   If the GWA prompt is consistent, Cline executes the task, adapting as necessary.
3.  Upon task completion (or after notifying the user of a conflict), Cline uses `attempt_completion` with:
    *   A `<result>` summarizing the actions taken and their outcome.
    *   A separate, clearly marked block containing the message to be relayed back to GWA. This message should concisely inform GWA of the task completion and any relevant outcomes or state changes.

## Knowledge Base Structure

*   `/kb/common/`: General policies and procedures applicable across the project.
*   `/kb/<agent_name>/`: Policies, procedures, and knowledge specific to a particular internal agent (e.g., `/kb/config_agent/`).
*   `/tracking/`: Contains files for tracking project status, like `action_items.md`.
*   `C:/ABRIDER/ASA/kb/common/README.md`: Location for sensitive or environment-specific common knowledge (outside the main repository).
