import asyncio
import json
import websockets
from typing import Dict, Any

async def connect_mcp():
    """Connect to MCP server and demonstrate basic functionality."""
    uri = "ws://localhost:8000/ws"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to MCP server")

        # List available tools
        await websocket.send(json.dumps({
            "type": "list_tools"
        }))
        response = await websocket.recv()
        print("\nAvailable tools:")
        print(json.dumps(json.loads(response), indent=2))

        # Send a message
        await websocket.send(json.dumps({
            "type": "message",
            "message": "Hello, MCP!"
        }))
        response = await websocket.recv()
        print("\nMessage response:")
        print(json.dumps(json.loads(response), indent=2))

        # Use echo tool
        await websocket.send(json.dumps({
            "type": "tool",
            "tool": "echo",
            "parameters": {
                "message": "Testing echo tool"
            }
        }))
        response = await websocket.recv()
        print("\nEcho tool response:")
        print(json.dumps(json.loads(response), indent=2))

        # Use time tool
        await websocket.send(json.dumps({
            "type": "tool",
            "tool": "get_time",
            "parameters": {}
        }))
        response = await websocket.recv()
        print("\nTime tool response:")
        print(json.dumps(json.loads(response), indent=2))

        # Use calculator tool
        await websocket.send(json.dumps({
            "type": "tool",
            "tool": "calculate",
            "parameters": {
                "operation": "add",
                "a": 5,
                "b": 3
            }
        }))
        response = await websocket.recv()
        print("\nCalculator tool response:")
        print(json.dumps(json.loads(response), indent=2))

if __name__ == "__main__":
    print("Starting MCP client demo...")
    asyncio.run(connect_mcp())