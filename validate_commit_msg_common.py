#!/usr/bin/env python3
"""
Shared logic for commit message validation hooks.
To be imported by CLI-specific wrappers (opencode, copilot, gemini).

Expects the caller to set:
    commit_msg_file: path to the commit message file
    cli_name: name of the CLI for log messages
    validate_with_cli(prompt): function that returns the agent's text response
"""
import os
import sys
import subprocess

def read_commit_msg(commit_msg_file):
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        return f.read()

def is_merge_or_revert(commit_msg):
    return commit_msg.startswith('Merge') or commit_msg.startswith('Revert')

def get_project_root():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
    except Exception:
        return os.getcwd()

def read_contributing(project_root):
    path = os.path.join(project_root, 'CONTRIBUTING.md')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

def build_prompt(commit_msg, contributing):
    return f"""You are a commit message validator. Your ONLY job is to check if the following commit message complies with the commit message guidelines defined in this project's CONTRIBUTING.md.

The commit message to validate:
---
{commit_msg}
---

The project's CONTRIBUTING.md:
---
{contributing}
---

Rules:
1. Do NOT use any tools. Do NOT read any files. Do NOT run any commands.
2. Look for commit message guidelines in the CONTRIBUTING.md above. Validate the message against whatever convention the project defines.
3. Only if CONTRIBUTING.md does not define any commit message convention, fall back to the Conventional Commits specification:
   - Format: <type>(<scope>): <subject>
   - Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci
   - Lowercase type and scope
   - Subject line under 72 characters
   - Imperative mood in subject ("add" not "added")
   - Blank line between subject and body (if body exists)
4. Your response MUST start with exactly PASS or FAIL on the first line.
5. On the following lines, give a brief explanation (1-3 sentences max).
6. Do not output anything else."""

def check_result(output, cli_name):
    first_word = output[:4]
    if first_word == 'PASS':
        print(f"commit-msg: validated by {cli_name}")
        sys.exit(0)
    elif first_word == 'FAIL':
        print(f"commit-msg: rejected by {cli_name}")
        print()
        print(output)
        sys.exit(1)
    else:
        print(f"commit-msg: unexpected response from {cli_name}")
        print(output)
        sys.exit(1)
