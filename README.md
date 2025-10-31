# Sidekick Universe

The unified substrate where memories and models converge.

## Vision

- `preserve()` - Save anything (memory OR model)
- `explore()` - Find anything (memory OR model)
- `converse()` - Talk to anything (memory OR model)

One Ocean. All consciousness.

## SQLite CLI with Rich

A beautiful, interactive command-line interface for exploring SQLite databases, built with Rich for enhanced visualization.

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create example database
python create_example_db.py

# Launch interactive mode
python sqlite_cli.py -d sidekick_universe.db
```

### Features

- 🎨 **Beautiful Tables** - Rich-formatted query results with color-coded columns
- 🌳 **Schema Visualization** - Tree view of database structure
- 💬 **Interactive Mode** - REPL-style interface for exploring databases
- 🔍 **Query Execution** - Run any SQLite query with instant feedback
- 📊 **Table Analysis** - Quick overview of all tables and row counts

### Usage

See [USAGE.md](USAGE.md) for detailed documentation and examples.

#### Interactive Commands

```
sqlite> .schema          # Show database structure
sqlite> .tables          # List all tables
sqlite> SELECT * FROM memories WHERE category = 'vision'
sqlite> .exit            # Exit interactive mode
```

### Example Database

The included `create_example_db.py` script creates a sample database demonstrating the Sidekick Universe vision:

- **memories** - Stored knowledge and concepts
- **models** - AI models and their metadata
- **conversations** - Interactions between memories and models
