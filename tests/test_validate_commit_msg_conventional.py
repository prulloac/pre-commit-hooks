"""
Unit tests for validate_commit_msg_conventional.py
Covers the main() function and its validation logic for Conventional Commits.
"""
import os
import sys
import tempfile
import pytest
from pre_commit_hooks import validate_commit_msg_conventional

# Helper to invoke main with a temp file

def run_main_with_message(msg):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tf:
        tf.write(msg)
        tf.flush()
        tf_name = tf.name
    try:
        sys_argv_backup = sys.argv[:]
        sys.argv = ['validate_commit_msg_conventional.py', tf_name]
        try:
            validate_commit_msg_conventional.main()
        except SystemExit as e:
            return e.code
        finally:
            sys.argv = sys_argv_backup
    finally:
        os.remove(tf_name)

# Test: Accepts valid Conventional Commit message
# Purpose: Should exit 0 for a valid message

def test_valid_conventional_commit():
    msg = "feat(auth): add OAuth login\n\nBody text."
    assert run_main_with_message(msg) == 0

# Test: Rejects invalid type
# Purpose: Should exit 1 for an invalid type

def test_invalid_type():
    msg = "feature(auth): add OAuth login"
    assert run_main_with_message(msg) == 1

# Test: Accepts message with no scope
# Purpose: Should exit 0 for a valid type and subject, no scope

def test_valid_no_scope():
    msg = "fix: correct typo"
    assert run_main_with_message(msg) == 0

# Test: Rejects missing subject
# Purpose: Should exit 1 if subject is missing

def test_missing_subject():
    msg = "fix:"
    assert run_main_with_message(msg) == 1

# Test: Accepts Merge and Revert commits
# Purpose: Should exit 0 for Merge and Revert messages

def test_merge_and_revert():
    assert run_main_with_message("Merge branch 'main'") == 0
    assert run_main_with_message("Revert \"something\"") == 0

# Test: Requires blank line between subject and body
# Purpose: Should exit 1 if no blank line between subject and body

def test_requires_blank_line_between_subject_and_body():
    msg = "feat(core): add feature\nBody without blank line"
    assert run_main_with_message(msg) == 1

# Test: Accepts message with exclamation mark for breaking change
# Purpose: Should exit 0 for breaking change syntax

def test_breaking_change():
    msg = "feat(core)!: breaking change\n\nBody"
    assert run_main_with_message(msg) == 0
