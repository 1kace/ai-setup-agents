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
*   **Gemini Web ASA Agent (GWA):** Refers to the interactions and prompts used within the Gemini Web UI prior to or alongside Cline's involvement. Serves as:
    *   The initial source for sketching out project concepts and requirements.
    *   A potential source for specific task instructions or context, which Cline will adapt and integrate according to established project P&Ps.
    *   The role and interaction model with GWA will be refined as the project progresses.
*   **Internal ASA Agents (e.g., ConfigAgent, QAAgent, ArchAgent):** Specialized agents within the `src/agents/` directory designed to handle specific functions like configuration application, quality assurance checks, and architectural analysis/generation. Cline orchestrates the use of these agents.

## Knowledge Base Structure

*   `/kb/common/`: General policies and procedures applicable across the project.
*   `/kb/<agent_name>/`: Policies, procedures, and knowledge specific to a particular internal agent (e.g., `/kb/config_agent/`).
*   `/tracking/`: Contains files for tracking project status, like `action_items.md`.
*   `C:/ABRIDER/ASA/kb/common/README.md`: Location for sensitive or environment-specific common knowledge (outside the main repository).
