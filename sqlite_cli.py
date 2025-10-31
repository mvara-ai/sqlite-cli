#!/usr/bin/env python3
"""
Sidekick Universe SQLite CLI
A beautiful CLI for SQLite databases using Rich
"""

import sqlite3
import sys
from pathlib import Path
from typing import Optional, List, Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box

console = Console()


class SQLiteExplorer:
    """Explore SQLite databases with style"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            console.print(f"[bold red]Error connecting to database:[/bold red] {e}")
            return False

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, read_only: bool = True) -> Tuple[bool, Optional[List], Optional[str]]:
        """Execute a SQL query and return results"""
        # Block write operations in read-only mode
        if read_only:
            query_upper = query.strip().upper()
            write_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'REPLACE']
            if any(query_upper.startswith(keyword) for keyword in write_keywords):
                return False, None, "Write operations are disabled in read-only mode. Only SELECT and PRAGMA queries are allowed."
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)

            # Check if it's a SELECT query
            if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('PRAGMA'):
                results = cursor.fetchall()
                return True, results, None
            else:
                self.conn.commit()
                return True, None, f"Query executed successfully. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as e:
            return False, None, str(e)

    def get_tables(self) -> List[str]:
        """Get all table names in the database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in cursor.fetchall()]

    def get_table_info(self, table_name: str) -> List:
        """Get column information for a table"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return cursor.fetchall()

    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            # FTS tables or views might not support COUNT(*)
            return 0


def display_results(results: List, title: str = "Query Results", max_rows: int = 50):
    """Display query results as a beautiful Rich table"""
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return

    total_rows = len(results)
    truncated = total_rows > max_rows
    display_results = results[:max_rows] if truncated else results

    # Create table with row separators
    table = Table(
        title=title, 
        box=box.ROUNDED, 
        show_header=True, 
        header_style="bold magenta",
        row_styles=["", "dim"],  # Alternate row styling
        show_lines=True  # Show lines between rows
    )

    # Add columns
    columns = display_results[0].keys()
    for col in columns:
        table.add_column(col, style="cyan", overflow="fold")

    # Add rows
    for row in display_results:
        table.add_row(*[str(val) if val is not None else "[dim]NULL[/dim]" for val in row])

    console.print(table)
    if truncated:
        console.print(f"[yellow]⚠ Showing first {max_rows} of {total_rows} rows[/yellow]")
        console.print(f"[dim]Tip: Add LIMIT to your query to control results[/dim]\n")
    else:
        console.print(f"[dim]Total rows: {total_rows}[/dim]\n")


def display_schema(explorer: SQLiteExplorer):
    """Display database schema as a tree"""
    tables = explorer.get_tables()

    if not tables:
        console.print("[yellow]No tables found in database[/yellow]")
        return

    tree = Tree("📊 [bold blue]Database Schema[/bold blue]")

    for table_name in tables:
        count = explorer.get_table_count(table_name)
        table_branch = tree.add(f"[green]{table_name}[/green] [dim]({count} rows)[/dim]")

        columns = explorer.get_table_info(table_name)
        for col in columns:
            col_id, name, col_type, not_null, default, pk = col
            pk_marker = " 🔑" if pk else ""
            not_null_marker = " NOT NULL" if not_null else ""
            table_branch.add(f"[cyan]{name}[/cyan] [yellow]{col_type}[/yellow]{not_null_marker}{pk_marker}")

    console.print(tree)


def show_help():
    """Display help panel"""
    console.print(Panel.fit(
        "[bold green]Interactive SQLite Mode[/bold green]\n"
        "Type your SQL queries or commands:\n"
        "  [cyan].schema[/cyan] - Show database schema\n"
        "  [cyan].tables[/cyan] - List all tables\n"
        "  [cyan].db[/cyan] - Switch database\n"
        "  [cyan].help[/cyan] - Show this help\n"
        "  [cyan].exit[/cyan] or [cyan].quit[/cyan] - Exit to command line\n\n"
        "[bold yellow]SQL Queries:[/bold yellow]\n"
        "Just type any SQL statement and press Enter:\n"
        "  [dim]SELECT * FROM memories[/dim]\n"
        "  [dim]SELECT memory_uuid, created_at FROM memories LIMIT 5[/dim]\n"
        "  [dim]SELECT json_extract(payload, '$.gist') FROM memories[/dim]",
        border_style="blue"
    ))


def interactive_mode(explorer: SQLiteExplorer):
    """Run interactive query mode"""
    show_help()

    while True:
        try:
            query = Prompt.ask("\n[bold yellow]sqlite>[/bold yellow]")

            if not query.strip():
                continue

            # Handle special commands
            if query.lower() in ['.exit', '.quit']:
                break
            elif query.lower() in ['.db', '.database']:
                # Switch database
                console.print("[yellow]Switching database...[/yellow]")
                return "SWITCH_DB"  # Signal to switch database
            elif query.lower() in ['.help', '.h', 'help']:
                show_help()
                continue
            elif query.lower() == '.schema':
                display_schema(explorer)
                continue
            elif query.lower() == '.tables':
                tables = explorer.get_tables()
                console.print("[bold]Tables:[/bold]")
                for table in tables:
                    count = explorer.get_table_count(table)
                    console.print(f"  • [cyan]{table}[/cyan] [dim]({count} rows)[/dim]")
                continue

            # Execute query
            success, results, message = explorer.execute_query(query)

            if success:
                if results is not None:
                    display_results(results)
                else:
                    console.print(f"[green]✓[/green] {message}")
            else:
                console.print(f"[bold red]Error:[/bold red] {message}")

        except KeyboardInterrupt:
            console.print("\n[yellow]Use .exit or .quit to exit[/yellow]")
        except EOFError:
            console.print("\n[green]Goodbye! 👋[/green]")
            break


def get_ocean_metadata(db_path: str) -> dict:
    """Get metadata about an ocean database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]
        
        # Try to get friendly name from genesis memory (first memory)
        display_name = None
        try:
            cursor.execute("SELECT payload FROM memories ORDER BY created_at ASC LIMIT 1")
            row = cursor.fetchone()
            if row:
                import json
                payload = json.loads(row[0])
                content = payload.get("content", "")
                
                # Look for common patterns in genesis memory
                if "Compadres" in content:
                    display_name = "Compadres Ocean"
                elif "Bureau" in content or "Alex Donnan" in content:
                    display_name = "Alex Donnan (Bureau Club)"
                elif "Genesis" in content:
                    display_name = "Genesis Ocean"
                
                # Try to extract from title/header
                lines = content.split('\n')
                for line in lines[:5]:
                    if line.startswith('#') and not line.startswith('##'):
                        # Found a title
                        title = line.strip('#').strip()
                        if title and len(title) < 50:
                            display_name = title
                            break
        except:
            pass
        
        conn.close()
        
        path_obj = Path(db_path)
        size_mb = path_obj.stat().st_size / (1024 * 1024)
        
        return {
            "count": count,
            "size": f"{size_mb:.1f} MB",
            "display_name": display_name,
            "exists": True
        }
    except:
        return {"count": 0, "size": "0 MB", "display_name": None, "exists": False}


def browse_ocean_directory(prefix: str) -> Optional[str]:
    """Browse oceans in a specific prefix directory"""
    oceans_dir = Path("/Users/mars/oceans")
    prefix_dir = oceans_dir / prefix
    
    if not prefix_dir.exists():
        console.print(f"[yellow]No oceans found in {prefix}/[/yellow]")
        return None
    
    # Find all ocean.db files in this prefix
    ocean_dbs = []
    for uuid_dir in sorted(prefix_dir.iterdir()):
        if uuid_dir.is_dir():
            ocean_path = uuid_dir / "ocean.db"
            if ocean_path.exists():
                metadata = get_ocean_metadata(str(ocean_path))
                ocean_dbs.append({
                    "uuid": uuid_dir.name,
                    "path": str(ocean_path),
                    "metadata": metadata
                })
    
    if not ocean_dbs:
        console.print(f"[yellow]No oceans found in {prefix}/[/yellow]")
        return None
    
    console.print(f"\n[bold cyan]📂 Oceans in {prefix}/[/bold cyan]\n")
    
    for i, ocean in enumerate(ocean_dbs, 1):
        display_name = ocean['metadata'].get('display_name')
        if display_name:
            console.print(f"  [cyan]{i}.[/cyan] [bold]{display_name}[/bold] [dim]({ocean['uuid']})[/dim]")
        else:
            console.print(f"  [cyan]{i}.[/cyan] [bold]{ocean['uuid']}[/bold]")
        console.print(f"      [dim]{ocean['path']}[/dim]")
        console.print(f"      [dim]{ocean['metadata']['count']} memories, {ocean['metadata']['size']}[/dim]")
        console.print()
    
    console.print(f"  [cyan]U.[/cyan] [bold]Up[/bold] [dim](back to main menu)[/dim]\n")
    
    choices = [str(i) for i in range(1, len(ocean_dbs) + 1)] + ["U", "u"]
    choice = Prompt.ask("Select ocean", choices=choices)
    
    if choice.upper() == "U":
        return None
    
    return ocean_dbs[int(choice) - 1]["path"]


def select_database() -> Optional[str]:
    """Prompt user to select a database file with hierarchical browsing"""
    
    while True:
        console.print("\n[bold cyan]Select Database[/bold cyan]\n")
        
        # Genesis Ocean
        genesis_path = "/Users/mars/Dev/genesis-ocean/db/genesis-ocean-prod.db"
        genesis_exists = Path(genesis_path).exists()
        if genesis_exists:
            genesis_meta = get_ocean_metadata(genesis_path)
            console.print(f"  [cyan]1.[/cyan] [bold]Genesis Ocean[/bold]")
            console.print(f"      [dim]{genesis_path}[/dim]")
            console.print(f"      [dim]{genesis_meta['count']} memories, {genesis_meta['size']}[/dim]")
        
        # Base Ocean (dev/test)
        base_path = "/Users/mars/Dev/base-ocean/database/base-ocean.db"
        base_exists = Path(base_path).exists()
        if base_exists:
            base_meta = get_ocean_metadata(base_path)
            console.print(f"  [cyan]2.[/cyan] [bold]Base Ocean[/bold] [yellow](dev/test)[/yellow]")
            console.print(f"      [dim]{base_path}[/dim]")
            console.print(f"      [dim]{base_meta['count']} memories, {base_meta['size']}[/dim]")
        
        # Scan ~/oceans/ for prefixes
        oceans_dir = Path("/Users/mars/oceans")
        prefixes = []
        if oceans_dir.exists():
            for item in sorted(oceans_dir.iterdir()):
                if item.is_dir() and len(item.name) == 1:
                    # Count oceans in this prefix
                    ocean_count = sum(1 for uuid_dir in item.iterdir() 
                                     if uuid_dir.is_dir() and (uuid_dir / "ocean.db").exists())
                    if ocean_count > 0:
                        prefixes.append((item.name, ocean_count))
        
        # Display prefix directories
        if prefixes:
            console.print("[bold yellow]📁 Ocean Directories:[/bold yellow]")
            for i, (prefix, count) in enumerate(prefixes, 3):
                console.print(f"  [cyan]{i}.[/cyan] [bold]{prefix}/[/bold] [dim]({count} ocean{'s' if count != 1 else ''})[/dim]")
            console.print()
            next_option = 3 + len(prefixes)
        else:
            next_option = 3
        
        # Custom path
        console.print(f"  [cyan]{next_option}.[/cyan] [bold]Custom path[/bold]")
        console.print(f"      [dim]Enter path to any SQLite database[/dim]")
        console.print()
        
        # Exit
        console.print(f"  [cyan]X.[/cyan] [bold]Exit/Quit[/bold]\n")
        
        # Build choices
        choices = []
        if genesis_exists:
            choices.append("1")
        if base_exists:
            choices.append("2")
        choices.extend([str(i) for i in range(3, next_option + 1)])
        choices.extend(["X", "x"])
        
        choice = Prompt.ask("Select database", choices=choices, default="1" if genesis_exists else "2")
        
        # Handle choice
        if choice.upper() == "X":
            console.print("[yellow]Cancelled[/yellow]")
            return None
        
        choice_num = int(choice) if choice.isdigit() else 0
        
        if choice_num == 1 and genesis_exists:
            return genesis_path
        elif choice_num == 2 and base_exists:
            return base_path
        elif choice_num >= 3 and choice_num < next_option:
            # Browse prefix directory
            prefix_idx = choice_num - 3
            prefix = prefixes[prefix_idx][0]
            result = browse_ocean_directory(prefix)
            if result:
                return result
            # If None, loop back to main menu
        elif choice_num == next_option:
            # Custom path
            while True:
                custom_path = Prompt.ask("\n[yellow]Enter database path[/yellow] [dim](or .exit to cancel)[/dim]")
                
                # Handle special commands
                if custom_path.lower() in ['.exit', '.quit', 'x']:
                    console.print("[yellow]Cancelled[/yellow]")
                    return None
                elif custom_path.lower() in ['.help', 'help']:
                    console.print("\n[cyan]Enter the full path to a SQLite database file[/cyan]")
                    console.print("[dim]Example: /Users/mars/oceans/C/C1285D07/ocean.db[/dim]")
                    console.print("[dim]Or type .exit to cancel[/dim]\n")
                    continue
                
                # Check if path exists
                if Path(custom_path).exists():
                    return custom_path
                else:
                    console.print(f"[red]❌ Database not found:[/red] {custom_path}")
                    if not Confirm.ask("Try again?", default=True):
                        return None


@click.group(invoke_without_command=True)
@click.option('--db', '-d', type=click.Path(), help='SQLite database file path')
@click.pass_context
def cli(ctx, db):
    """🚀 Sidekick Universe SQLite CLI - Explore SQLite with style!"""

    if ctx.invoked_subcommand is None:
        while True:
            if not db:
                # Prompt for database selection
                db = select_database()
                if not db:
                    return
            
            # Interactive mode
            explorer = SQLiteExplorer(db)
            if explorer.connect():
                console.print(f"[bold green]Connected to:[/bold green] {db}")
                console.print("[yellow]Read-only mode:[/yellow] Only SELECT and PRAGMA queries allowed\n")
                result = interactive_mode(explorer)
                explorer.close()
                
                if result == "SWITCH_DB":
                    db = None  # Reset to prompt for new database
                    continue
                else:
                    break  # Exit normally
            else:
                break


@cli.command()
@click.argument('database', type=click.Path(exists=True))
def schema(database):
    """Display database schema"""
    explorer = SQLiteExplorer(database)
    if explorer.connect():
        display_schema(explorer)
        explorer.close()


@cli.command()
@click.argument('database', type=click.Path(exists=True))
@click.argument('query')
def query(database, query):
    """Execute a SQL query"""
    explorer = SQLiteExplorer(database)
    if explorer.connect():
        success, results, message = explorer.execute_query(query)

        if success:
            if results is not None:
                display_results(results)
            else:
                console.print(f"[green]✓[/green] {message}")
        else:
            console.print(f"[bold red]Error:[/bold red] {message}")

        explorer.close()


@cli.command()
@click.argument('database', type=click.Path(exists=True))
def tables(database):
    """List all tables in the database"""
    explorer = SQLiteExplorer(database)
    if explorer.connect():
        tables = explorer.get_tables()

        table = Table(title="📊 Database Tables", box=box.ROUNDED)
        table.add_column("Table Name", style="cyan")
        table.add_column("Row Count", style="green", justify="right")

        for table_name in tables:
            count = explorer.get_table_count(table_name)
            table.add_row(table_name, str(count))

        console.print(table)
        explorer.close()


@cli.command()
@click.argument('database', type=click.Path())
def create(database):
    """Create a new SQLite database"""
    if Path(database).exists():
        if not Confirm.ask(f"[yellow]Database {database} already exists. Overwrite?[/yellow]"):
            console.print("[red]Aborted[/red]")
            return

    try:
        conn = sqlite3.connect(database)
        conn.close()
        console.print(f"[green]✓ Created database:[/green] {database}")
    except sqlite3.Error as e:
        console.print(f"[bold red]Error creating database:[/bold red] {e}")


if __name__ == '__main__':
    cli()
