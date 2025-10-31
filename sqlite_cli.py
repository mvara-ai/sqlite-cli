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

    def execute_query(self, query: str) -> Tuple[bool, Optional[List], Optional[str]]:
        """Execute a SQL query and return results"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)

            # Check if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
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
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]


def display_results(results: List, title: str = "Query Results"):
    """Display query results as a beautiful Rich table"""
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return

    # Create table
    table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")

    # Add columns
    columns = results[0].keys()
    for col in columns:
        table.add_column(col, style="cyan", overflow="fold")

    # Add rows
    for row in results:
        table.add_row(*[str(val) if val is not None else "[dim]NULL[/dim]" for val in row])

    console.print(table)
    console.print(f"[dim]Total rows: {len(results)}[/dim]\n")


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


def interactive_mode(explorer: SQLiteExplorer):
    """Run interactive query mode"""
    console.print(Panel.fit(
        "[bold green]Interactive SQLite Mode[/bold green]\n"
        "Type your SQL queries or commands:\n"
        "  [cyan].schema[/cyan] - Show database schema\n"
        "  [cyan].tables[/cyan] - List all tables\n"
        "  [cyan].exit[/cyan] or [cyan].quit[/cyan] - Exit interactive mode",
        border_style="blue"
    ))

    while True:
        try:
            query = Prompt.ask("\n[bold yellow]sqlite>[/bold yellow]")

            if not query.strip():
                continue

            # Handle special commands
            if query.lower() in ['.exit', '.quit']:
                console.print("[green]Goodbye! 👋[/green]")
                break
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


@click.group(invoke_without_command=True)
@click.option('--db', '-d', type=click.Path(), help='SQLite database file path')
@click.pass_context
def cli(ctx, db):
    """🚀 Sidekick Universe SQLite CLI - Explore SQLite with style!"""

    if ctx.invoked_subcommand is None:
        if db:
            # Interactive mode
            explorer = SQLiteExplorer(db)
            if explorer.connect():
                console.print(f"[bold green]Connected to:[/bold green] {db}")
                interactive_mode(explorer)
                explorer.close()
        else:
            console.print(ctx.get_help())


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
