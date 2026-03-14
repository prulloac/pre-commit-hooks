#!/usr/bin/env python3
"""
Commit message validation hook using Gemini CLI.
Imports shared logic from validate_commit_msg_common.py.
"""
import sys
import shutil
import subprocess
import json
from validate_commit_msg_common import (
    read_commit_msg, is_merge_or_revert, get_project_root, read_contributing, build_prompt, check_result
)

def validate_with_cli(prompt):
    try:
        result = subprocess.run([
            'gemini', '-p', prompt, '-o', 'json'
        ], capture_output=True, text=True, check=False)
        raw = result.stdout.strip()
        # Try to parse JSON and extract the response
        try:
            responses = json.loads(raw)
            for item in responses:
                if item.get('type') == 'response':
                    return item.get('response', raw)
        except Exception:
            # Fallback: try to extract text manually
            import re
            m = re.search(r'"response":"(.*?)"', raw)
            if m:
                return m.group(1).replace('\\n', '\n')
        return raw
    except Exception as e:
        return f"FAIL\nException running gemini: {e}"

def main():
    cli_name = "gemini"
    if len(sys.argv) < 2:
        print("commit-msg: missing commit message file argument")
        sys.exit(1)
    commit_msg_file = sys.argv[1]
    if not shutil.which('gemini'):
        print("WARNING: gemini not found, skipping commit message validation")
        sys.exit(0)
    commit_msg = read_commit_msg(commit_msg_file)
    if is_merge_or_revert(commit_msg):
        sys.exit(0)
    project_root = get_project_root()
    contributing = read_contributing(project_root)
    prompt = build_prompt(commit_msg, contributing)
    output = validate_with_cli(prompt)
    check_result(output, cli_name)

if __name__ == "__main__":
    main()
