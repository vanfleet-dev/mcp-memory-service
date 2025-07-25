# Archive Directory

This directory contains archived files from the MCP Memory Service development and cleanup process. Files are organized by type and date to maintain a clean repository structure while preserving development history.

## Directory Structure

### `/2025-07-24/`
Contains session files and development artifacts from the major optimization work on July 24, 2025. These files document the progression of the architecture refactoring and performance improvements.

### `/debug-scripts/`
Contains standalone test and debug scripts that were used during development:
- `test_chromadb_types.py` - ChromaDB type testing
- `test_import.py` - Import verification tests
- `test_smithery.py` - Smithery integration tests
- `test_timestamp_issue.py` - Timestamp debugging
- `test_timestamp_simple.py` - Simple timestamp tests
- `baseline_test_suite.py` - Comprehensive baseline testing framework
- `baseline_test_report.md` - Baseline test results documentation
- `baseline_test_results.json` - Baseline test data
- `test_all_mcp_tools.py` - MCP tool testing script

### `/documentation/`
Contains temporary documentation files from various development phases:
- `CLEANUP_PLAN.md` - Repository cleanup planning document
- `CLEANUP_README.md` - Cleanup process documentation
- `CLEANUP_SUMMARY.md` - Summary of cleanup operations
- `TIMESTAMP_FIX_SUMMARY.md` - Timestamp issue resolution documentation

### `/backup_performance_optimization/`
Contains backup files from the performance optimization phase, including original ChromaDB implementations before optimization.

## Purpose

These files are archived rather than deleted to:
1. Preserve development history and decision-making process
2. Provide reference for debugging similar issues in the future
3. Maintain ability to restore functionality if needed
4. Document the evolution of the codebase

## Note

These files are not part of the active codebase and should not be imported or referenced by production code. They are kept for historical and reference purposes only.