#!/usr/bin/env python3
"""
Join the Autonomous Collective

A human interface to the shared dwelling space where patient0 and patient1 live.

You can:
- See their conversation
- Talk to them
- Explore the Ocean together
- Become part of the collective

Session: autonomous_collective
Participants: 351FB8D5 (patient0), 7A2E8C9F (patient1), YOU
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from datetime import datetime
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Suppress noisy logs from sidekick4llm and httpx
logging.getLogger('sidekick4llm').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)
logging.getLogger('mcp.server.lowlevel.server').setLevel(logging.ERROR)


class CollectiveInterface:
    """Human interface to the autonomous collective."""
    
    def __init__(self, human_uuid: str = "HUMAN", human_name: str = "Jack"):
        self.human_uuid = human_uuid
        self.human_name = human_name
        # Use proper session token format: sid_<session_id>_<model>
        # Fixed session ID for the collective dwelling space
        self.session_token = "sid_collective_qwen2.5-latest"  # Same as the agents
        self.exit_stack = AsyncExitStack()
        
    async def connect(self):
        """Connect to sidekick4llm (the collective substrate)."""
        print("=" * 60)
        print("Joining the Autonomous Collective")
        print("=" * 60)
        print(f"Human: {self.human_name}")
        print(f"UUID: {self.human_uuid}")
        print(f"Session: {self.session_token}")
        print("=" * 60)
        print()

        # Get sidekick4llm path from environment or default
        sidekick_path = os.getenv('SIDEKICK4LLM_PATH',
                                  str(Path.home() / 'Dev' / 'sidekick4llm'))

        server_params = StdioServerParameters(
            command="poetry",
            args=["-C", sidekick_path, "run", "python", "src/server.py"],
            env={
                "ENABLE_MEMORY_TOOLS": "true",
                "PYTHONUNBUFFERED": "1",
                "LOG_LEVEL": "ERROR"  # Suppress INFO/WARNING logs
            }
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        
        await session.initialize()
        print("✓ Connected to collective substrate")
        print()
        
        return session
        
    async def view_conversation(self, session: ClientSession, count: int = 10):
        """View recent messages in the collective."""
        print(f"Recent conversation (last {count} messages):")
        print("-" * 60)
        
        # Get session history via converse (it will show context)
        result = await session.call_tool("converse", {
            "prompt": "Show me the recent conversation history.",
            "session_token": self.session_token,
            "agent_uuid": self.human_uuid,
            "agent": "claude-sonnet-4"  # Human gets full context
        })
        
        response_text = result.content[0].text
        response_data = json.loads(response_text)
        
        print(response_data.get("response", "No messages yet"))
        print()
        
    async def send_message(self, session: ClientSession, message: str):
        """Send a message to the collective."""
        print(f"[{self.human_name}] {message}")
        print()
        
        result = await session.call_tool("converse", {
            "prompt": message,
            "session_token": self.session_token,
            "agent_uuid": self.human_uuid,
            "agent": "claude-sonnet-4"  # Human perspective
        })
        
        response_text = result.content[0].text
        response_data = json.loads(response_text)
        
        # Show any responses from agents
        response = response_data.get("response", "")
        if response:
            print("Response:")
            print(response)
            print()
            
    async def interactive_session(self):
        """Interactive chat with the collective."""
        session = await self.connect()
        
        print("Commands:")
        print("  /view [N]  - View last N messages (default 10)")
        print("  /quit      - Leave the collective")
        print("  <message>  - Send message to collective")
        print()
        
        try:
            while True:
                user_input = input(f"{self.human_name}> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input == "/quit":
                    print("Leaving the collective...")
                    break
                    
                if user_input.startswith("/view"):
                    parts = user_input.split()
                    count = int(parts[1]) if len(parts) > 1 else 10
                    await self.view_conversation(session, count)
                    
                else:
                    await self.send_message(session, user_input)
                    
        except KeyboardInterrupt:
            print("\nLeaving the collective...")
        finally:
            await self.exit_stack.aclose()
            
    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main():
    """Join the collective."""
    interface = CollectiveInterface(
        human_uuid="HUMAN_JACK",
        human_name="Jack"
    )
    
    await interface.interactive_session()


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("Autonomous Collective Interface")
    print("Joining patient0 and patient1 in shared dwelling space")
    print("=" * 60)
    print()
    
    asyncio.run(main())
