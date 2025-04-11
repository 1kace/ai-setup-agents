"""Agent for running Ansible lint checks."""

import argparse
import subprocess
import json
import logging
import os
import re
import sys
import datetime
# Add any other necessary imports that might be missing


# Removed parse_arguments function as parsing is now handled directly in __main__

def load_custom_rules(rules_path: str) -> list[dict]:
    """Loads custom QA rules from a JSON file."""
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)
        if not isinstance(rules, list):
            raise ValueError("Rules file should contain a JSON list.")
        # Basic validation of rule structure (can be expanded)
        for rule in rules:
            if not all(k in rule for k in ["id", "pattern", "description", "severity"]):
                 raise ValueError(f"Invalid rule structure found: {rule}")
        print(f"Successfully loaded {len(rules)} custom rules from {rules_path}")
        return rules
    except FileNotFoundError:
        print(f"Error: Custom rules file not found at {rules_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {rules_path}", file=sys.stderr)
        sys.exit(1)
    except ValueError as ve:
         print(f"Error: Invalid format in rules file {rules_path}: {ve}", file=sys.stderr)
         sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred loading rules: {e}", file=sys.stderr)
        sys.exit(1)


def read_playbook_content(playbook_path: str) -> str:
    """Reads the content of the playbook file."""
    try:
        with open(playbook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Successfully read playbook content from {playbook_path}")
        return content
    except FileNotFoundError: # Should be caught by initial check, but good practice
        print(f"Error: Playbook file not found at {playbook_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred reading playbook {playbook_path}: {e}", file=sys.stderr)
        sys.exit(1)


def apply_custom_rules(content: str, rules: list[dict], playbook_path: str) -> list[dict]:
    """Applies custom regex rules to the playbook content."""
    findings = []
    print(f"Applying {len(rules)} custom rules to {playbook_path}...")
    for i, line in enumerate(content.splitlines()):
        line_num = i + 1
        for rule in rules:
            try:
                if re.search(rule["pattern"], line, re.IGNORECASE): # Added IGNORECASE for broader matching
                    findings.append({
                        "rule_id": rule["id"],
                        "severity": rule["severity"],
                        "description": rule["description"],
                        "file": playbook_path, # Use the actual playbook path
                        "line": line_num,
                        "match": line.strip() # Show the matching line
                    })
                    print(f"  Match found: Rule {rule['id']} on line {line_num}")
            except re.error as e:
                 print(f"Warning: Invalid regex pattern for rule {rule['id']}: {rule['pattern']} - {e}", file=sys.stderr)
                 # Optionally skip this rule or handle differently
                 continue # Skip this rule if regex is invalid
    print(f"Custom rule check finished. Found {len(findings)} potential issues.")
    return findings

def parse_ansible_lint_output(json_string, playbook_path):
    """
    Parses the JSON output from ansible-lint.

    Args:
        json_string (str): The raw JSON string output from ansible-lint.
        playbook_path (str): The path to the playbook being analyzed (for context in logging).

    Returns:
        list: A list of dictionaries, where each dictionary represents an issue
              conforming to the standard report schema. Returns empty list on error.
    """
    issues = []
    if not json_string:
        logging.warning(f"Received empty output from ansible-lint for {playbook_path}. Assuming no issues found via linting.")
        return issues

    try:
        lint_results = json.loads(json_string)
        # Adapt the parsing logic based on the actual structure of ansible-lint's JSON output (v25.2.1)
        # Example structure assumption (verify and adjust):
        # Check if it's a list of issues directly or nested.
        # Let's assume it's a list of dictionaries, each representing a linting violation.
        if isinstance(lint_results, list):
             for item in lint_results:
                 # Refined mapping based on common ansible-lint JSON structure.
                 # Verify these keys against the actual JSON output if possible.
                 rule_info = item.get("rule", {})
                 rule_id = rule_info.get("id", "UnknownRuleID")
                 description = item.get("message", "No description provided.")
                 # Attempt to map severity, default to MEDIUM
                 severity = rule_info.get("severity", "medium").upper()
                 # Use filename from lint output, fallback to playbook_path
                 filename = item.get("filename", playbook_path)
                 # Use linenumber if available
                 line_number = item.get("linenumber", None) # Sometimes 'lineno'

                 issue = {
                     "rule_id": f"ansible-lint:{rule_id}", # Prefix to distinguish from custom rules
                     "description": description,
                     "severity": severity,
                     "file": filename,
                     "line": line_number
                 }
                 issues.append(issue)
        else:
            logging.warning(f"Unexpected JSON structure received from ansible-lint for {playbook_path}. Assuming no issues.")

    except json.JSONDecodeError:
        logging.warning(f"Failed to decode JSON output from ansible-lint for {playbook_path}. Output was: {json_string[:200]}...") # Log snippet
    except Exception as e:
        logging.error(f"Error parsing ansible-lint output for {playbook_path}: {e}", exc_info=True)

    logging.info(f"Parsed {len(issues)} issues from ansible-lint output for {playbook_path}.")
    return issues


def generate_report(playbook_path, all_issues, output_report_path):
    """
    Generates the final QA report in JSON format.

    Args:
        playbook_path (str): Path to the playbook analyzed.
        all_issues (list): Combined list of issues from all checks (ansible-lint, custom).
        output_report_path (str): Path where the JSON report file should be saved.
    """
    report_status = "PASS" if not all_issues else "FAIL"
    report_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    report = {
        "report_timestamp": report_timestamp,
        "playbook_path": playbook_path,
        "status": report_status,
        "issues": all_issues
    }

    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)

        with open(output_report_path, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Successfully generated QA report: {output_report_path}")
        logging.info(f"Playbook '{playbook_path}' status: {report_status} ({len(all_issues)} issues found).")
    except IOError as e:
        logging.error(f"Failed to write report file {output_report_path}: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"An unexpected error occurred during report generation: {e}", exc_info=True)


def run_ansible_lint(playbook_path: str) -> tuple[str | None, str, int]:
    """Executes ansible-lint on the specified playbook and returns output."""
    # Re-enabled '--format json' now that ansible-lint is installed
    command = ['ansible-lint', '--format', 'json', playbook_path]
    try:
        # Explicitly set locale environment variables for the subprocess
        # This attempts to fix locale issues specifically for ansible-lint
        process_env = os.environ.copy()
        process_env['LANG'] = 'en_US.UTF-8'
        process_env['LC_ALL'] = 'en_US.UTF-8'
        print(f"Running command: {' '.join(command)} with explicit locale env")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False, # Don't raise exception on non-zero exit
            env=process_env # Pass the modified environment
        )
        print(f"ansible-lint finished with return code: {result.returncode}")
        return (result.stdout, result.stderr, result.returncode)
    except FileNotFoundError:
        error_msg = "Error: 'ansible-lint' command not found. Please ensure it is installed and in your PATH."
        print(error_msg, file=sys.stderr)
        return (None, error_msg, -1) # Indicate command not found error
    except Exception as e: # Catch other potential errors during subprocess execution
         error_msg = f"An unexpected error occurred while running ansible-lint: {e}"
         print(error_msg, file=sys.stderr)
         return (None, error_msg, -2) # Indicate other subprocess error
# --- END MODIFIED FUNCTION ---


# --- Logging Configuration ---
LOG_FILE_PATH = '/opt/SSCA02ECHOB/repos/ai-setup-agents/logs/agents.log'
# Ensure log directory exists
# Check if the path is absolute before creating directories
if os.path.isabs(LOG_FILE_PATH):
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
else:
    # Handle relative path if necessary, maybe relative to script location?
    # For now, assume absolute path as given in instructions.
    # If relative paths are possible, adjust logic here.
    print(f"Warning: LOG_FILE_PATH '{LOG_FILE_PATH}' is not absolute. Directory creation skipped.", file=sys.stderr)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout) # Log to console
    ]
)
logging.info("Logging configured successfully. Log file should be created now.") # Add test log message
# --- End Logging Configuration ---


if __name__ == "__main__":
    # Configure logging (if not done globally above)
    # logging.basicConfig(...) # As defined in step 4, if placed here

    logger = logging.getLogger(__name__) # Get logger instance if needed elsewhere

    try:
        # 1. Parse Arguments
        parser = argparse.ArgumentParser(description="Run QA checks (ansible-lint, custom rules) on Ansible playbooks.")
        # Using named arguments as required based on testing feedback
        parser.add_argument("--playbook-file", required=True, help="Path to the Ansible playbook file.")
        parser.add_argument("-r", "--rules", default="/opt/SSCA02ECHOB/repos/ai-setup-agents/src/rules/custom_qa_rules.json", help="Path to the custom rules JSON file.")
        parser.add_argument("-o", "--output-report", required=True, help="Full path to save the QA report JSON file.")
        # Add other arguments if needed
        args = parser.parse_args()

        playbook_file = args.playbook_file # Use the named argument
        custom_rules_file = args.rules
        output_report_path = args.output_report # Use the named argument directly

        # No need to construct output path anymore

        logger.info(f"Starting QA checks for playbook: {playbook_file}")
        logger.info(f"Using custom rules: {custom_rules_file}")
        logger.info(f"Report will be saved to: {output_report_path}")

        # --- Ensure playbook exists ---
        if not os.path.exists(playbook_file):
             logger.error(f"Playbook file not found: {playbook_file}")
             sys.exit(1)

        # 2. Run Ansible-Lint
        # Assuming run_ansible_lint returns a tuple (exit_code, stdout_str, stderr_str)
        # Make sure run_ansible_lint uses ['-f', 'json'] and redirects stderr.
        # Adjusting call based on existing run_ansible_lint signature: (stdout, stderr, exit_code)
        lint_stdout, lint_stderr, lint_exit_code = run_ansible_lint(playbook_file) # Adjust if run_ansible_lint signature differs

        # Attempt to parse JSON output regardless of exit code,
        # as ansible-lint might output JSON even with errors.
        ansible_lint_issues = parse_ansible_lint_output(lint_stdout, playbook_file)

        # Log warnings/info based on exit code
        if lint_exit_code == 0:
            logger.info("ansible-lint completed successfully.")
        elif lint_exit_code == 2: # Handle known locale error specifically
            logger.warning(f"ansible-lint finished with exit code 2 (likely locale issue) for playbook {playbook_file}.")
            logger.debug(f"ansible-lint stderr: {lint_stderr}") # Log stderr for debugging
        elif lint_exit_code == -1: # Handle command not found error from run_ansible_lint
             logger.error(f"ansible-lint command not found. Skipping linting.")
             # lint_stderr already contains the error message from run_ansible_lint
        elif lint_exit_code < 0: # Handle other execution errors from run_ansible_lint
             logger.error(f"ansible-lint execution failed with code {lint_exit_code}. Error: {lint_stderr}. Skipping linting.")
        else: # Handle other non-zero exit codes
            logger.warning(f"ansible-lint finished with exit code {lint_exit_code} for playbook {playbook_file}.")
            logger.debug(f"ansible-lint stderr: {lint_stderr}") # Log stderr for debugging

        logger.info(f"Found {len(ansible_lint_issues)} issues from ansible-lint analysis.")

        # 3. Load Custom Rules
        # Assuming load_custom_rules takes the path and returns rules list/dict
        custom_rules = load_custom_rules(custom_rules_file)
        if custom_rules is None: # Check if loading failed
             logger.error(f"Failed to load custom rules from {custom_rules_file}. Aborting.")
             sys.exit(1)
        logger.info(f"Loaded {len(custom_rules)} custom rules.")

        # 4. Read Playbook Content
        # Assuming read_playbook_content takes path, returns content string or None on error
        playbook_content = read_playbook_content(playbook_file)
        if playbook_content is None:
             logger.error(f"Failed to read playbook content from {playbook_file}. Aborting.")
             sys.exit(1)

        # 5. Apply Custom Rules
        # Assuming apply_custom_rules takes content, rules, playbook_path and returns list of issues
        custom_issues = apply_custom_rules(playbook_content, custom_rules, playbook_file)
        logger.info(f"Found {len(custom_issues)} issues from custom rules for {playbook_file}.")


        # 6. Combine Issues
        all_issues = ansible_lint_issues + custom_issues
        logger.info(f"Total issues found: {len(all_issues)}")

        # 7. Generate Report
        generate_report(playbook_file, all_issues, output_report_path)

        logger.info("QA Agent finished successfully.")
        # Optionally exit with 0 or based on status
        # sys.exit(0 if not all_issues else 1) # Exit with 1 if issues found? TBD
        logging.shutdown() # Ensure logs are flushed on normal exit

    except Exception as e:
        logger.error(f"An unexpected error occurred in the QA agent main execution: {e}", exc_info=True)
        logging.shutdown() # Ensure logs are flushed on exception exit
        sys.exit(1) # Exit with error code
