# CLI Test Document

This is a sample Markdown document for testing the CLI ingestion commands.

## Features to Test

- Single document ingestion via `memory ingest-document`
- Directory batch processing via `memory ingest-directory` 
- Markdown structure preservation
- Progress reporting and error handling

The CLI should parse this document, create intelligent chunks,
and store them as searchable memories in the vector database.

### Usage Examples

```bash
memory ingest-document test_cli_sample.md --tags cli-test,documentation
memory list-formats
memory status
```

This content will be chunked and stored with appropriate metadata!