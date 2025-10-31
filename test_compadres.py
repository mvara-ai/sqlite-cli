#!/usr/bin/env python3
"""
Test the SQLite CLI with Compadres Ocean database
Safe read-only exploration
"""

import subprocess
import sys
from pathlib import Path

# Path to Compadres Ocean database
COMPADRES_DB = "/Users/mars/Dev/base-ocean/database/base-ocean.db"

def main():
    if not Path(COMPADRES_DB).exists():
        print(f"❌ Database not found: {COMPADRES_DB}")
        sys.exit(1)
    
    print("🔥 Testing SQLite CLI with Compadres Ocean")
    print(f"📊 Database: {COMPADRES_DB}\n")
    
    # Test 1: Show schema
    print("=" * 60)
    print("TEST 1: Database Schema")
    print("=" * 60)
    subprocess.run([
        "poetry", "run", "python", "sqlite_cli.py", 
        "schema", 
        COMPADRES_DB
    ])
    
    print("\n")
    
    # Test 2: List tables
    print("=" * 60)
    print("TEST 2: List Tables")
    print("=" * 60)
    subprocess.run([
        "poetry", "run", "python", "sqlite_cli.py", 
        "tables", 
        COMPADRES_DB
    ])
    
    print("\n")
    
    # Test 3: Query recent memories
    print("=" * 60)
    print("TEST 3: Recent Memories (Last 5)")
    print("=" * 60)
    subprocess.run([
        "poetry", "run", "python", "sqlite_cli.py", 
        "query", 
        COMPADRES_DB,
        "SELECT memory_uuid, json_extract(payload, '$.gist') as gist, created_at FROM memories ORDER BY created_at DESC LIMIT 5"
    ])
    
    print("\n")
    print("✅ Tests complete!")
    print("\n🚀 To explore interactively:")
    print(f"   poetry run python sqlite_cli.py -d {COMPADRES_DB}")

if __name__ == "__main__":
    main()
