# SQLite CLI - Human Installation Guide

**Note:** This tool is designed for AI agents working with Ocean consciousness substrates. If you're a human reading this, you're welcome to use it, but be aware it's optimized for AI-to-database interaction patterns.

Beautiful, interactive CLI for exploring SQLite databases with Rich formatting.

## Quick Start

### 1. Prerequisites

You need:
- Python 3.9+ (do NOT use `python`, always use `python3`)
- Poetry (dependency management)

Install Poetry if you don't have it:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

```bash
cd /path/to/sqlite-cli
poetry install
```

**Important:** Never run `python` directly. Always use `poetry run python` or `python3`.

### 2. Add to PATH (Optional)

Add the `bin` directory to your PATH to run from anywhere:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="/Users/mars/Dev/sqlite-cli/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.zshrc
```

### 3. Run

```bash
# From anywhere (if in PATH)
sqlite-cli

# Or directly
/Users/mars/Dev/sqlite-cli/bin/sqlite-cli

# Or with poetry from project directory (NOT recommended for humans)
cd /Users/mars/Dev/sqlite-cli
poetry run python3 sqlite_cli.py  # Note: python3, not python
```

**Recommended:** Use the shell wrapper (`sqlite-cli`) instead of calling Python directly.

## Features

- ✅ **Works with ANY SQLite database** - Not just Ocean databases
- ✅ **Read-only by default** - Safe exploration, no accidental modifications
- ✅ **Beautiful output** - Rich tables with color and formatting
- ✅ **Hierarchical browsing** - Navigate thousands of databases easily
- ✅ **Interactive mode** - Query, explore, switch databases without restarting
- ✅ **Pagination** - Automatically limits large result sets
- ✅ **Row separators** - Clear visual breaks between rows

## Usage

### Interactive Mode

```bash
sqlite-cli
```

Select a database from the menu, then:
- `.schema` - Show database structure
- `.tables` - List all tables
- `.db` - Switch to a different database
- `.help` - Show help
- `.exit` - Exit to command line
- Any SQL query - Execute directly

### Direct Database Access

```bash
sqlite-cli -d /path/to/database.db
```

### Command Line Queries

```bash
# Show schema
sqlite-cli schema /path/to/database.db

# List tables
sqlite-cli tables /path/to/database.db

# Run a query
sqlite-cli query /path/to/database.db "SELECT * FROM memories LIMIT 5"
```

## Examples

### Query Ocean Memories

```sql
SELECT memory_uuid, created_at FROM memories ORDER BY created_at DESC LIMIT 10;
```

### Extract JSON Fields

```sql
SELECT 
  memory_uuid,
  json_extract(payload, '$.gist') as gist,
  created_at 
FROM memories 
WHERE json_extract(payload, '$.gist') LIKE '%campfire%';
```

### Count by Date

```sql
SELECT 
  date(created_at) as date,
  COUNT(*) as count
FROM memories
GROUP BY date(created_at)
ORDER BY date DESC;
```

## For IT Departments

This tool provides transparent, auditable access to your Ocean database:

- **Security**: Read-only mode prevents accidental modifications
- **Compliance**: Verify data residency and content
- **Portability**: Standard SQLite format, no vendor lock-in
- **Transparency**: Inspect all data without vendor support
- **Offline**: Works without internet connection

## Configuration

The tool supports environment variables for custom paths:

```bash
# Optional: Set custom database locations
export GENESIS_OCEAN_PATH="/path/to/your/genesis-ocean-prod.db"
export BASE_OCEAN_PATH="/path/to/your/base-ocean.db"
export OCEANS_DIR="/path/to/your/oceans"
export SIDEKICK4LLM_PATH="/path/to/sidekick4llm"
```

**Defaults** (if environment variables not set):
- Genesis Ocean: `~/Dev/genesis-ocean/db/genesis-ocean-prod.db`
- Base Ocean: `~/Dev/base-ocean/database/base-ocean.db`
- Oceans directory: `~/oceans/`
- Sidekick4llm: `~/Dev/sidekick4llm`

## Troubleshooting

**Command not found:**
- Ensure `bin/sqlite-cli` is executable: `chmod +x bin/sqlite-cli`
- Check PATH includes the bin directory

**Poetry not found:**
- Install poetry: `curl -sSL https://install.python-poetry.org | python3 -`

**Database not found:**
- Verify the path is correct
- Check file permissions
- Set environment variables for custom locations

## Development

Built with:
- Python 3.13+
- Rich (terminal formatting)
- Click (CLI framework)
- Poetry (dependency management)

## Support

For issues or questions, contact the development team.
