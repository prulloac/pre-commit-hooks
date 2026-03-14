#!/usr/bin/env python3
"""
Commit message validation hook enforcing max subject length.
"""
import sys
import os

def main():
    commit_msg_file = ''
    max_length_input = '128'
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            commit_msg_file = arg
        elif arg.isdigit():
            max_length_input = arg
    if not commit_msg_file or not os.path.isfile(commit_msg_file):
        print("commit-msg: could not read commit message file")
        sys.exit(1)
    if not max_length_input.isdigit() or int(max_length_input) <= 0:
        print(f"commit-msg: invalid max length '{max_length_input}' (must be a positive integer)")
        sys.exit(1)
    max_length = int(max_length_input)
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    first_line = lines[0].rstrip('\n') if lines else ''
    if first_line.startswith('Merge') or first_line.startswith('Revert'):
        sys.exit(0)
    if len(first_line) > max_length:
        print(f"commit-msg: rejected (subject line exceeds {max_length} characters)")
        print(f"Length: {len(first_line)}")
        sys.exit(1)
    print(f"commit-msg: validated (subject line <= {max_length} chars)")
    sys.exit(0)

if __name__ == "__main__":
    main()
