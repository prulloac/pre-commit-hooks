# pre-commit-hooks

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A collection of custom Git commit message validation hooks for use with [pre-commit](https://pre-commit.com/).

## Overview

This repository provides several shell-based hooks to validate commit messages according to different rules and standards. These hooks are designed to be used with the pre-commit framework and can be integrated into your workflow to enforce commit message quality and consistency.

## Available Hooks

- **validate-commit-msg-common**: Shared logic for commit message validation, sourced by other hooks.
- **validate-commit-msg-conventional**: Enforces [Conventional Commits](https://www.conventionalcommits.org/) format using regex rules.
- **validate-commit-msg-copilot**: Uses GitHub Copilot CLI to validate commit messages with AI assistance.
- **validate-commit-msg-gemini**: Uses Gemini CLI to validate commit messages with AI assistance.
- **validate-commit-msg-max**: Enforces a maximum subject line length for commit messages.
- **validate-commit-msg-opencode**: Uses OpenCode CLI to validate commit messages with AI assistance.

## Usage

1. **Add this repository as a submodule or copy the `pre-commit-hooks` directory into your project.**
2. **Create or update your `.pre-commit-config.yaml` in your project root:**

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-commit-msg-conventional
        name: Validate Commit Message (Conventional)
        entry: pre-commit-hooks/validate-commit-msg-conventional.sh
        language: script
        stages: [commit-msg]
      # Add other hooks as needed
```

3. **Install pre-commit and the hooks:**

```sh
pip install pre-commit
pre-commit install --hook-type commit-msg
```

4. **(Optional) Run the hooks manually:**

```sh
pre-commit run --hook-stage commit-msg --all-files
```

## Requirements
- [pre-commit](https://pre-commit.com/)
- Bash shell
- For Copilot/Gemini/OpenCode hooks: the respective CLI tools must be installed and available in your PATH

## License

MIT License
