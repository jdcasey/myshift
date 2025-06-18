#!/bin/bash

# Exit on any error
# set -e

echo "🔍 Running PR preflight checks..."

echo -e "\n📝 Formatting code..."
echo "Running black..."
black --check --line-length 120 .
echo "Running isort..."
isort --check-only --line-length 120 .

echo -e "\n🔒 Running security checks..."
echo "Running bandit..."
bandit -r myshift/

# echo "Running safety..."
# safety scan

echo -e "\n🧪 Running tests..."
pytest

# echo -e "\n✅ All checks passed!" 