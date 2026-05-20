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
  echo "4) poetry run mypy src/   # Type check with mypy"
  echo "5) poetry run ruff check src/  # Lint with ruff"
  echo "6) poetry shell           # Activate Poetry shell"
  echo "7) poetry run <cmd>       # Run custom command"
  echo "8) Safe commit flow       # add + pre-commit + add + commit"
  echo "0) Exit"
}

while true; do
  show_menu
  read -p $'\nChoose an option: ' opt
  case $opt in
    1) poetry install ;;
    2) poetry run pytest ;;
    3) poetry run pre-commit run --all-files ;;
    4) poetry run mypy src/ ;;
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
    0) echo "Exiting."; exit 0 ;;
    *) echo "Invalid option." ;;
  esac
done
