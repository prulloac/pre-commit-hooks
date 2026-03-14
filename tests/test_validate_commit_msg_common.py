import os
import subprocess
import pytest

import pre_commit_hooks.validate_commit_msg_common as vcmc

def test_read_commit_msg(tmp_path):
    msg = "test commit message"
    file = tmp_path / "msg.txt"
    file.write_text(msg, encoding="utf-8")
    assert vcmc.read_commit_msg(str(file)) == msg

def test_is_merge_or_revert():
    assert vcmc.is_merge_or_revert("Merge branch 'main'")
    assert vcmc.is_merge_or_revert("Revert \"something\"")
    assert not vcmc.is_merge_or_revert("feat: add feature")

def test_get_project_root(monkeypatch):
    # Simulate git failure, fallback to cwd
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: (_ for _ in ()).throw(Exception()))
    cwd = os.getcwd()
    assert vcmc.get_project_root() == cwd

    # Simulate git success
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: "/mock/root\n")
    assert vcmc.get_project_root() == "/mock/root"

def test_read_contributing(tmp_path):
    # No file
    assert vcmc.read_contributing(str(tmp_path)) == ''
    # With file
    file = tmp_path / "CONTRIBUTING.md"
    content = "rules here"
    file.write_text(content, encoding="utf-8")
    assert vcmc.read_contributing(str(tmp_path)) == content

def test_build_prompt():
    commit_msg = "feat: add x"
    contributing = "Use Conventional Commits"
    prompt = vcmc.build_prompt(commit_msg, contributing)
    assert commit_msg in prompt
    assert contributing in prompt
    assert prompt.startswith("You are a commit message validator.")

def test_check_result_pass(monkeypatch, capsys):
    with pytest.raises(SystemExit) as e:
        vcmc.check_result("PASS\nAll good", "cli")
    out = capsys.readouterr().out
    assert "validated by cli" in out
    assert e.value.code == 0

def test_check_result_fail(monkeypatch, capsys):
    with pytest.raises(SystemExit) as e:
        vcmc.check_result("FAIL\nBad message", "cli")
    out = capsys.readouterr().out
    assert "rejected by cli" in out
    assert "Bad message" in out
    assert e.value.code == 1

def test_check_result_unexpected(monkeypatch, capsys):
    with pytest.raises(SystemExit) as e:
        vcmc.check_result("???\nWhat?", "cli")
    out = capsys.readouterr().out
    assert "unexpected response" in out
    assert e.value.code == 1
