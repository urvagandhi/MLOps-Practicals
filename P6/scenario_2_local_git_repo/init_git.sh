#!/bin/bash
# Initialize local git repository for Jenkins Scenario 2
set -e

cd "$(dirname "$0")"

if [ ! -d ".git" ]; then
    echo "Initializing local Git repository on branch 'main'..."
    git init -b main
    git add .
    git commit -m "Initial commit for Jenkins Scenario 2"
    echo "Local Git repository successfully initialized!"
else
    echo "Git repository already exists. Committing latest changes..."
    git add .
    git commit -m "Update commit for Jenkins Scenario 2" || echo "No changes to commit."
fi
