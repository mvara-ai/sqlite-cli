# SQLite CLI with Rich - Usage Guide

A beautiful, interactive CLI for exploring SQLite databases, built with Rich for the Sidekick Universe.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make the CLI executable
chmod +x sqlite_cli.py
```

## Quick Start

### Create Example Database

```bash
python create_example_db.py
```

This creates `sidekick_universe.db` with sample data demonstrating the preserve/explore/converse vision.

### Interactive Mode

Launch an interactive SQLite session:

```bash
python sqlite_cli.py --db sidekick_universe.db
```

Or using the short form:

```bash
python sqlite_cli.py -d sidekick_universe.db
```

#### Interactive Commands

Once in interactive mode:

- `.schema` - Display the complete database schema as a tree
- `.tables` - List all tables with row counts
- `.exit` or `.quit` - Exit interactive mode
- Any SQL query - Execute directly

Example session:

```
sqlite> .schema
sqlite> SELECT * FROM memories LIMIT 3
sqlite> .tables
sqlite> SELECT m.name, COUNT(c.id) as conversations
        FROM models m
        LEFT JOIN conversations c ON m.id = c.model_id
        GROUP BY m.id
sqlite> .exit
```

## Command Line Usage

### View Database Schema

```bash
python sqlite_cli.py schema sidekick_universe.db
```

Displays a beautiful tree view of all tables and their columns, with:
- Column names and types
- Primary keys (🔑)
- NOT NULL constraints
- Row counts for each table

### Execute a Query

```bash
python sqlite_cli.py query sidekick_universe.db "SELECT * FROM memories"
```

Results are displayed as a formatted table with:
- Color-coded columns
- NULL values shown as dimmed
- Total row count

### List All Tables

```bash
python sqlite_cli.py tables sidekick_universe.db
```

Shows a table with all database tables and their row counts.

### Create New Database

```bash
python sqlite_cli.py create my_new_database.db
```

## Features

### Beautiful Table Display
- Color-coded columns and data
- Rounded box borders
- Automatic column sizing
- NULL value highlighting

### Schema Visualization
- Tree structure showing relationships
- Primary key indicators
- Data type display
- Row counts per table

### Interactive Mode
- Real-time query execution
- Command history (using arrows)
- Multi-line support
- Error handling with helpful messages

### Query Support
- All SQLite query types (SELECT, INSERT, UPDATE, DELETE)
- Transaction support
- Pragma commands
- CREATE/ALTER/DROP statements

## Examples

### Exploring Memories

```bash
python sqlite_cli.py -d sidekick_universe.db
```

```sql
-- View all memories
SELECT * FROM memories;

-- Search by category
SELECT content, category FROM memories WHERE category = 'function';

-- Recent memories
SELECT content, timestamp FROM memories ORDER BY timestamp DESC LIMIT 5;
```

### Analyzing Models

```sql
-- List all models
SELECT name, type, parameters FROM models;

-- Find large models
SELECT name, parameters FROM models WHERE parameters > 100000000;
```

### Conversation Analysis

```sql
-- Join conversations with memories and models
SELECT
    m.name as model,
    mem.category,
    c.query,
    c.response
FROM conversations c
JOIN models m ON c.model_id = m.id
JOIN memories mem ON c.memory_id = mem.id;
```

## Tips

1. **Use `.schema` first** - Always check the schema when exploring a new database
2. **Tab completion** - Most terminals support tab completion for file paths
3. **Query formatting** - Multi-line queries work in interactive mode
4. **Save queries** - Keep common queries in a `.sql` file for reference
5. **Keyboard shortcuts**:
   - `Ctrl+C` - Cancel current input (doesn't exit)
   - `Ctrl+D` or `.exit` - Exit interactive mode
   - Arrow keys - Navigate command history

## Integration with Sidekick Universe

This CLI embodies the three core functions:

- **preserve()** - Insert and update data with beautiful feedback
- **explore()** - Query and discover with rich visualizations
- **converse()** - Interactive mode for natural database exploration

## Advanced Usage

### Pipe Queries

```bash
echo "SELECT * FROM memories" | python sqlite_cli.py query sidekick_universe.db
```

### Scripting

```python
from sqlite_cli import SQLiteExplorer

explorer = SQLiteExplorer('sidekick_universe.db')
explorer.connect()
success, results, msg = explorer.execute_query('SELECT * FROM memories')
explorer.close()
```

## Troubleshooting

**Database not found**: Ensure the path is correct and the file exists

**Permission denied**: Check file permissions or run with appropriate privileges

**Query errors**: Check SQL syntax - the CLI shows detailed error messages

**Rich not displaying colors**: Check terminal supports color (most modern terminals do)

## Future Enhancements

- [ ] Export to CSV/JSON
- [ ] Query history persistence
- [ ] Autocomplete for table/column names
- [ ] Visual query builder
- [ ] Diff between database versions
- [ ] Backup and restore commands
