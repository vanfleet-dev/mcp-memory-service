# Memory Cleanup Example: A Practical Guide

This guide demonstrates how to effectively use the MCP-Memory-Service to identify and clean up obsolete memories, based on a real cleanup operation performed on July 20, 2025.

## Table of Contents
- [Overview](#overview)
- [Step 1: Assess Database Health](#step-1-assess-database-health)
- [Step 2: Identify Memory Categories](#step-2-identify-memory-categories)
- [Step 3: Search for Cleanup Candidates](#step-3-search-for-cleanup-candidates)
- [Step 4: Analyze and Categorize](#step-4-analyze-and-categorize)
- [Step 5: Execute Cleanup](#step-5-execute-cleanup)
- [Step 6: Document the Operation](#step-6-document-the-operation)
- [Best Practices](#best-practices)

## Overview

Memory cleanup is an essential maintenance task for keeping your MCP-Memory-Service database optimized and relevant. This example shows how to systematically identify, categorize, and remove obsolete memories while preserving important information.

## Step 1: Assess Database Health

Start by checking the current state of your database:

```python
# Check database health and statistics
memory:check_database_health
```

**Example output:**
```json
{
  "statistics": {
    "collection": {
      "total_memories": 321,
      "embedding_function": "SentenceTransformerEmbeddingFunction"
    },
    "storage": {
      "size_mb": 19.94
    }
  }
}
```

## Step 2: Identify Memory Categories

Check for duplicate memories first:

```python
# Check for duplicates
memory:cleanup_duplicates
```

Then explore different time periods to understand memory patterns:

```python
# Check recent memories
memory:recall_memory(n_results=20, query="last week")
memory:recall_memory(n_results=20, query="last month")
```

## Step 3: Search for Cleanup Candidates

Search for common temporary or test content:

```python
# Search for test and debug memories
memory:search_by_tag(tags=["test", "testing", "debug", "debugging"])

# Search for temporary content
memory:search_by_tag(tags=["temporary", "temp", "draft", "old", "outdated", "obsolete"])
```

## Step 4: Analyze and Categorize

Based on the search results, categorize memories for cleanup:

### Categories Identified in This Example:

1. **Test and Debug Memories (12 memories)**
   - Simple test entries created for verification
   - Debug entries for timestamp testing
   - Performance benchmarking tests
   - Messages like "Test successful"

2. **Detailed MCP Debugging Logs (10 memories)**
   - Long technical debugging sessions
   - Handler registration problems
   - Protocol routing investigations
   - Issues that were already resolved

3. **Redundant Integration Updates (8 memories)**
   - Multiple "complete success" summaries
   - Repeated implementation status updates
   - Overlapping fix documentation

4. **Obsolete Technical Documentation (5 memories)**
   - Detailed fixes already in production
   - Superseded implementation details

### Cleanup Priority Framework:

- **Priority 1 - Safe to Delete:** Simple test memories with no long-term value
- **Priority 2 - Consider Consolidating:** Multiple entries about the same topic
- **Priority 3 - Keep but Archive:** Important technical solutions for reference

## Step 5: Execute Cleanup

Delete memories systematically by hash:

```python
# Delete individual memories
memory:delete_memory(content_hash="a2b93bd995946bf39b748120b38fbe751c2dd61ce141a8488acdb3a048f11107")
memory:delete_memory(content_hash="d8ba82c60ceafdc633671b1bc24a8c43241108e7cd0beb17d89618a659f92bac")
# ... continue for each identified memory
```

### Cleanup Results from This Example:
- **Deleted:** 15 obsolete memories
  - 9 test entries
  - 6 redundant debugging logs
- **Reduced:** From 321 to 306 memories
- **Preserved:** Important milestones, technical solutions, and documentation

## Step 6: Document the Operation

Always create a summary memory of the cleanup operation:

```python
memory:store_memory(
    content="""Memory Cleanup Operation Completed - July 20, 2025

    Successfully deleted 15 obsolete memories to optimize the database:
    - 9 simple test entries (tool verification, performance tests, debug tests)
    - 6 redundant MCP debugging logs (handler registration issues, TaskGroup errors)

    Database status after cleanup:
    - Total memories: 306 (reduced from 321)
    - Storage size: 19.94 MB
    - Database health: Excellent

    Preserved important memories:
    - Major milestones and achievements
    - Technical solutions and fixes
    - Project summaries and documentation""",
    metadata={"tags": ["cleanup", "optimization", "database-maintenance"], "type": "maintenance-report"}
)
```

## Best Practices

1. **Regular Maintenance**: Perform cleanup operations periodically to prevent database bloat

2. **Categorize Before Deleting**: Always analyze and categorize memories before deletion

3. **Preserve Important Information**: Keep memories that:
   - Document important solutions or fixes
   - Represent major milestones
   - Contain unique technical insights
   - May be referenced in the future

4. **Use Tags Effectively**: Tag memories appropriately to make future cleanup easier:
   - Use "test" for test entries
   - Use "debug" for debugging sessions
   - Use "temporary" for short-term content
   - Use "archive" for old but important content

5. **Document Cleanup Operations**: Always create a summary memory of what was cleaned up and why

6. **Verify After Cleanup**: Check database health after cleanup to ensure everything is working correctly

## Conclusion

This example demonstrates how the MCP-Memory-Service can be used for effective database maintenance. By following a systematic approach to identifying, categorizing, and removing obsolete memories, you can keep your memory database optimized and focused on valuable information.

The key is to balance thorough cleanup with preservation of potentially useful information, always documenting your actions for future reference.