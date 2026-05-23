#!/bin/bash
# helper.sh: Menu for common project commands
#
# To make this script executable, run:
#   chmod +x scripts/helper.sh
# Then run it with:
#   ./scripts/helper.sh

set -e

REPO_ROOT=""

ensure_repo_root() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "This command must be run inside a Git repository."
    return 1
  fi

  REPO_ROOT=$(git rev-parse --show-toplevel)
  cd "$REPO_ROOT"
}

get_hooks_dir() {
  local hooks_path
  hooks_path=$(git config --get core.hooksPath || true)

  if [[ -z "$hooks_path" ]]; then
    echo "$REPO_ROOT/.git/hooks"
  elif [[ "$hooks_path" = /* ]]; then
    echo "$hooks_path"
  else
    # Relative hooksPath is resolved from repository root.
    echo "$REPO_ROOT/$hooks_path"
  fi
}

show_hook_status() {
  ensure_repo_root

  local hooks_dir
  hooks_dir=$(get_hooks_dir)
  local hook_file="$hooks_dir/pre-commit"

  echo "Git hooks directory: $hooks_dir"

  if [[ -f "$hook_file" ]]; then
    echo "Pre-commit hook status: installed ($hook_file)"
  else
    echo "Pre-commit hook status: not installed"
  fi
}

install_or_repair_hooks() {
  ensure_repo_root

  if ! command -v poetry >/dev/null 2>&1; then
    echo "Poetry is not installed or not in PATH."
    return 1
  fi

  poetry run pre-commit install --install-hooks
  show_hook_status
}

bootstrap_after_clone() {
  echo "Running post-clone bootstrap..."

  ensure_repo_root

  if ! command -v poetry >/dev/null 2>&1; then
    echo "Poetry is not installed or not in PATH."
    return 1
  fi

  poetry install
  install_or_repair_hooks
  poetry run pre-commit run --all-files

  show_hook_status
  echo "Bootstrap complete. This operation is safe to run multiple times."
}

show_menu() {
  printf "\nCommon ai-taskflow project commands:\n"
  echo "1) poetry install         # Install dependencies"
  echo "2) poetry run pytest      # Run tests"
  echo "3) poetry run pre-commit run --all-files  # Run pre-commit on all files"
  echo "4) poetry run mypy src/ai_taskflow/core/config.py # Type check a specific file with mypy"
  echo "5) poetry run ruff check src/  # Lint with ruff"
  echo "6) poetry shell           # Activate Poetry shell"
  echo "7) poetry run <cmd>       # Run custom command"
  echo "8) Safe commit flow       # add + pre-commit + add + commit"
  echo "9) Install/repair hooks   # installs/repairs hook and shows status"
  echo "10) MyPy on all files     # Run mypy per-file to check entire codebase"
  echo "11) Bootstrap after clone # idempotent install + option 9 + full pre-commit"
  echo "12) Hook status           # Check whether pre-commit hook is installed"
  echo "0) Exit"
}

ensure_repo_root

while true; do
  show_menu
  read -p $'\nChoose an option: ' opt
  case $opt in
    1) poetry install ;;
    2) poetry run pytest ;;
    3) poetry run pre-commit run --all-files ;;
    4)
      read -p "Enter file path (default: src/ai_taskflow/core/config.py): " filepath
      if [[ -z "$filepath" ]]; then
        filepath="src/ai_taskflow/core/config.py"
      fi
      poetry run mypy "$filepath" --explicit-package-bases
      ;;
    5) poetry run ruff check src/ ;;
    6) poetry shell ;;
    7) read -p "Enter the command after 'poetry run ': " cmd; poetry run $cmd ;;
    8)
      read -p "Enter commit message: " commit_msg
      if [[ -z "$commit_msg" ]]; then
        echo "Commit message cannot be empty."
      else
        git add -A
        poetry run pre-commit run --all-files
        git add -A
        git commit -m "$commit_msg"
      fi
      ;;
    9) install_or_repair_hooks ;;
    10)
      echo "Running mypy on all Python files in src/ai_taskflow/..."
      python_files=$(find src/ai_taskflow -name "*.py" -type f | sort)
      if [[ -z "$python_files" ]]; then
        echo "No Python files found."
      else
        failed_count=0
        while IFS= read -r file; do
          if ! poetry run mypy "$file" --explicit-package-bases 2>&1 | grep -q "Success\|passed"; then
            ((failed_count++))
          fi
        done <<< "$python_files"
        echo "MyPy check complete. Failed: $failed_count file(s)"
      fi
      ;;
    11) bootstrap_after_clone ;;
    12) show_hook_status ;;
    0) echo "Exiting."; exit 0 ;;
    *) echo "Invalid option." ;;
  esac
done
