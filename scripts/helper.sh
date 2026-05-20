#!/bin/bash
# helper.sh: Menu for common project commands
#
# To make this script executable, run:
#   chmod +x scripts/helper.sh
# Then run it with:
#   ./scripts/helper.sh

set -e

show_menu() {
  echo "\nCommon ai-taskflow project commands:"
  echo "1) poetry install         # Install dependencies"
  echo "2) poetry run pytest      # Run tests"
  echo "3) poetry run pre-commit run --all-files  # Run pre-commit on all files"
    echo "4) poetry run mypy src/ai_taskflow/core/config.py # Type check a specific file with mypy"
  echo "5) poetry run ruff check src/  # Lint with ruff"
  echo "6) poetry shell           # Activate Poetry shell"
  echo "7) poetry run <cmd>       # Run custom command"
  echo "8) Safe commit flow       # add + pre-commit + add + commit"
  echo "9) Install/repair hooks   # pre-commit install --install-hooks"
    echo "10) MyPy on all files     # Run mypy per-file to check entire codebase"
  echo "0) Exit"
}

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
    9) poetry run pre-commit install --install-hooks ;;
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
    0) echo "Exiting."; exit 0 ;;
    *) echo "Invalid option." ;;
  esac
done
