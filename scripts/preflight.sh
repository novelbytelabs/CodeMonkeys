#!/bin/bash
# Preflight Script (Bootstrap)
#
# Runs all checks before commit/merge:
# 1. Pytest (schema validation tests)
# 2. Silverback validation (spec readiness + artifact validity)
# 3. Generate run report
#
# Usage:
#   ./scripts/preflight.sh [product_id]
#
# Example:
#   ./scripts/preflight.sh codemonkeys-dash

set -e

PRODUCT_ID="${1:-codemonkeys-dash}"
TEST_PATH="${2:-tests/dash/}"
CONDA_ENV="helios-gpu-118"

echo "============================================"
echo "  Code Monkeys Preflight (Bootstrap)"
echo "============================================"
echo "Product: $PRODUCT_ID"
echo "Test Path: $TEST_PATH"
echo ""

# Step 1: Run tests
echo "--- Step 1: Running Tests ---"
conda run -n "$CONDA_ENV" pytest "$TEST_PATH" -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Aborting preflight."
    exit 1
fi
echo ""

# Step 2: Silverback validation
echo "--- Step 2: Silverback Validation ---"
conda run -n "$CONDA_ENV" python scripts/silverback_validate.py --all
if [ $? -ne 0 ]; then
    echo "❌ Silverback validation failed. Aborting preflight."
    exit 1
fi
echo ""

# Step 3: Generate run report
echo "--- Step 3: Generating Run Report ---"
conda run -n "$CONDA_ENV" python scripts/generate_run_report.py "$PRODUCT_ID" --test-path "$TEST_PATH"
if [ $? -ne 0 ]; then
    echo "❌ Report generation failed. Aborting preflight."
    exit 1
fi
echo ""

echo "============================================"
echo "  ✅ Preflight PASSED"
echo "============================================"
echo ""
echo "Ready to commit/merge."
exit 0
