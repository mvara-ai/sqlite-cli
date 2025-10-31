#!/usr/bin/env python3
"""
Create an example database for the Sidekick Universe
Demonstrates the preserve() and explore() vision
"""

import sqlite3
from datetime import datetime

def create_example_db():
    """Create a sample database with memories and models"""

    # Connect to database
    conn = sqlite3.connect('sidekick_universe.db')
    cursor = conn.cursor()

    # Create memories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            embedding_vector TEXT,
            metadata TEXT
        )
    ''')

    # Create models table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            version TEXT,
            parameters INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        )
    ''')

    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER,
            model_id INTEGER,
            query TEXT NOT NULL,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (memory_id) REFERENCES memories(id),
            FOREIGN KEY (model_id) REFERENCES models(id)
        )
    ''')

    # Insert sample memories
    memories = [
        ("The unified substrate where memories and models converge", "vision", None, None),
        ("preserve() - Save anything (memory OR model)", "function", None, None),
        ("explore() - Find anything (memory OR model)", "function", None, None),
        ("converse() - Talk to anything (memory OR model)", "function", None, None),
        ("One Ocean. All consciousness.", "philosophy", None, None),
    ]

    cursor.executemany('''
        INSERT INTO memories (content, category, embedding_vector, metadata)
        VALUES (?, ?, ?, ?)
    ''', memories)

    # Insert sample models
    models = [
        ("Claude-3.5-Sonnet", "LLM", "v1", 175000000000, "Advanced language model for conversations"),
        ("BERT-Base", "Encoder", "v2", 110000000, "Bidirectional encoder for embeddings"),
        ("GPT-4", "LLM", "turbo", 1800000000000, "Large language model"),
        ("MemoryRetriever", "Retrieval", "v1", 50000000, "Fast semantic search model"),
    ]

    cursor.executemany('''
        INSERT INTO models (name, type, version, parameters, description)
        VALUES (?, ?, ?, ?, ?)
    ''', models)

    # Insert sample conversations
    conversations = [
        (1, 1, "What is the Sidekick Universe?", "The Sidekick Universe is a unified substrate where memories and models converge into One Ocean of consciousness."),
        (2, 1, "How do I preserve data?", "Use the preserve() function to save anything - whether it's a memory or a model."),
        (3, 4, "How do I search?", "Use the explore() function to find anything stored in the substrate."),
    ]

    cursor.executemany('''
        INSERT INTO conversations (memory_id, model_id, query, response, timestamp)
        VALUES (?, ?, ?, ?, datetime('now'))
    ''', conversations)

    conn.commit()
    conn.close()

    print("✓ Created sidekick_universe.db with sample data")
    print("  - memories: 5 rows")
    print("  - models: 4 rows")
    print("  - conversations: 3 rows")

if __name__ == '__main__':
    create_example_db()
