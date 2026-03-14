#!/usr/bin/env python3
"""
Commit message validation hook using Conventional Commits regex rules.
"""
import re
import sys
import os

def main():
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        print("commit-msg: could not read commit message file")
        sys.exit(1)
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        commit_msg = f.read()
    first_line = commit_msg.splitlines()[0] if commit_msg else ''
    if first_line.startswith('Merge') or first_line.startswith('Revert'):
        sys.exit(0)
    # Conventional Commits regex
    conventional_regex = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9][a-z0-9._/-]*\))?(!)?: .+$')
    if not conventional_regex.match(first_line):
        print("commit-msg: rejected (does not match Conventional Commits)")
        print()
        print("Expected: <type>(<scope>)?: <subject>")
        print("Example: feat(auth): add OAuth login")
        print("Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert")
        sys.exit(1)
    # If a body exists, require a blank line between subject and body
    lines = commit_msg.splitlines()
    if len(lines) > 1:
        second_line = lines[1]
        if second_line.strip():
            print("commit-msg: rejected (add a blank line between subject and body)")
            sys.exit(1)
    print("commit-msg: validated by conventional regex")
    sys.exit(0)

if __name__ == "__main__":
    main()
