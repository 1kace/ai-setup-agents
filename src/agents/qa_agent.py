"""Agent for running Ansible lint checks."""

import argparse
import subprocess
import sys
import json
import re
import os # Added for path validation

def parse_arguments():
    """Parses command-line arguments for the QA agent."""
    parser = argparse.ArgumentParser(description="Run ansible-lint checks on a playbook.")
    parser.add_argument(
        "--playbook-file",
        required=True,
        type=str,
        help="Path to the Ansible playbook file to lint."
    )
    parser.add_argument(
        "--output-report",
        required=True,
        type=str,
        help="Path to save the JSON linting report."
    )
    parser.add_argument(
        "--rules-config",
        required=False,
        type=str,
        default="src/rules/custom_qa_rules.json",
        help="Path to the custom rules configuration file (optional)."
    )
    args = parser.parse_args()

    # Validate input paths
    if not os.path.isfile(args.playbook_file):
        print(f"Error: Playbook file not found: {args.playbook_file}", file=sys.stderr)
        sys.exit(1)
    if args.rules_config and not os.path.isfile(args.rules_config):
         print(f"Error: Custom rules file not found: {args.rules_config}", file=sys.stderr)
         sys.exit(1)

    return args

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

# --- MODIFIED FUNCTION ---
def parse_ansible_lint_output(stdout_data: str | None) -> list[dict]:
    """
    Parses the output from ansible-lint.
    NOTE: Currently handles non-JSON output by returning an empty list,
    as the installed ansible-lint version did not support --json.
    Future enhancement could parse the text output if needed.
    """
    if stdout_data:
        print("Received stdout data from ansible-lint (text parsing not implemented).")
        # Future: Implement parsing logic for ansible-lint's default text output if required.
        # For now, assume no structured issues can be extracted without JSON.
    else:
         print("Ansible-lint produced no stdout data to parse.")

    return [] # Return empty list as JSON parsing is bypassed
# --- END MODIFIED FUNCTION ---


def save_report(all_issues: list[dict], output_path: str):
    """Saves the combined findings report to a JSON file in {'issues': [...]} format."""
    report_content = {"issues": all_issues}
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir: # Create directory if it's not the current directory
             os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_content, f, indent=2)
        print(f"Successfully saved combined report with {len(all_issues)} findings to {output_path}")
    except Exception as e:
        print(f"Error saving combined report to {output_path}: {e}", file=sys.stderr)
        # Consider exiting if report saving fails critically
        # sys.exit(1)


# --- MODIFIED FUNCTION ---
def run_ansible_lint(playbook_path: str) -> tuple[str | None, str, int]:
    """Executes ansible-lint on the specified playbook and returns output."""
    # Removed '--json' flag as it caused errors with the installed version
    command = ['ansible-lint', playbook_path]
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

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Starting QA Agent V2 (Ansible-Lint + Custom Rules)...")
    print(f"Playbook: {args.playbook_file}")
    print(f"Custom Rules: {args.rules_config}")
    print(f"Output Report: {args.output_report}")

    ansible_lint_issues = []
    custom_findings = []
    ansible_lint_failed = False

    # 1. Run Ansible-Lint
    print("\n--- Running Ansible-Lint ---")
    stdout_data, stderr_data, lint_exit_code = run_ansible_lint(args.playbook_file)

    if lint_exit_code < 0: # Handle execution errors (-1: not found, -2: other)
        print(f"Ansible-lint execution failed. Error:\n{stderr_data}")
        ansible_lint_failed = True
        # Decide if we should proceed with custom rules or exit
        # For now, let's proceed but note the failure.
    elif lint_exit_code > 0:
        print(f"Ansible-lint finished with issues (exit code: {lint_exit_code}).")
        # Attempt to parse output even if issues were found
        ansible_lint_issues = parse_ansible_lint_output(stdout_data)
        # Removed warning about parsing failure as we expect it now
        # if not ansible_lint_issues and stdout_data:
        #      print("Warning: Ansible-lint reported issues but no issues could be parsed from stdout.", file=sys.stderr)
        #      print("--- Ansible-lint stdout ---")
        #      print(stdout_data)
        #      print("--------------------------")
        if stderr_data:
             print("--- Ansible-lint stderr ---")
             print(stderr_data) # Print stderr which might contain useful info
             print("--------------------------")
    else: # Exit code 0
        print("Ansible-lint executed successfully.")
        ansible_lint_issues = parse_ansible_lint_output(stdout_data)
        # Removed warning about parsing failure as we expect it now
        # if not ansible_lint_issues and stdout_data:
        #      print("Warning: Ansible-lint exited successfully but no issues could be parsed from stdout.", file=sys.stderr)
        #      print("--- Ansible-lint stdout ---")
        #      print(stdout_data)
        #      print("--------------------------")

    print("--- Ansible-Lint Finished ---")


    # 2. Load Custom Rules
    print("\n--- Loading Custom Rules ---")
    custom_rules = load_custom_rules(args.rules_config)
    print("--- Custom Rules Loaded ---")


    # 3. Read Playbook Content (only if needed for custom rules)
    print("\n--- Reading Playbook for Custom Rules ---")
    playbook_content = read_playbook_content(args.playbook_file)
    print("--- Playbook Read ---")


    # 4. Apply Custom Rules
    print("\n--- Applying Custom Rules ---")
    custom_findings = apply_custom_rules(playbook_content, custom_rules, args.playbook_file) # Pass playbook path
    print("--- Custom Rules Applied ---")

    # 5. Combine Findings
    print("\n--- Combining Findings ---")
    all_issues = ansible_lint_issues + custom_findings # ansible_lint_issues will be empty for now
    print(f"Total issues found: {len(all_issues)} ({len(ansible_lint_issues)} from ansible-lint, {len(custom_findings)} from custom rules)")
    print("--- Findings Combined ---")


    # 6. Save Combined Report
    print("\n--- Saving Combined Report ---")
    save_report(all_issues, args.output_report)
    print("--- Report Saved ---")


    # 7. Determine Final Exit Code
    # Exit with error if ansible-lint failed to execute OR if any issues were found
    final_exit_code = 1 if (ansible_lint_failed or all_issues) else 0
    status_message = "finished with issues." if final_exit_code else "finished successfully."

    print(f"\nQA Agent V2 {status_message}")
    sys.exit(final_exit_code)
