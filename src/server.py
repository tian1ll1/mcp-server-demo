import json
import uuid
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from context.manager import ContextManager
from tools.basic_tools import ToolRegistry

app = FastAPI(title="MCP Server Demo")
context_manager = ContextManager()
tool_registry = ToolRegistry()

class MCPRequest(BaseModel):
    type: str
    tool: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """Connect a new client and return their session ID."""
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.active_connections[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str):
        """Disconnect a client."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send a message to a specific client."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)

connection_manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    session_id = await connection_manager.connect(websocket)
    context_manager.create_context(session_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            try:
                request = MCPRequest.parse_raw(data)
            except Exception as e:
                await connection_manager.send_message(session_id, {
                    "type": "error",
                    "message": f"Invalid request format: {str(e)}"
                })
                continue

            # Handle different request types
            if request.type == "message":
                if not request.message:
                    await connection_manager.send_message(session_id, {
                        "type": "error",
                        "message": "Message field is required for message type requests"
                    })
                    continue
                
                # Store message in context
                context_manager.add_message(session_id, "user", request.message)
                
                # Echo back for demo purposes
                await connection_manager.send_message(session_id, {
                    "type": "message",
                    "message": f"Received: {request.message}"
                })

            elif request.type == "tool":
                if not request.tool or not request.parameters:
                    await connection_manager.send_message(session_id, {
                        "type": "error",
                        "message": "Tool and parameters are required for tool type requests"
                    })
                    continue
                
                # Get tool
                tool = tool_registry.get_tool(request.tool)
                if not tool:
                    await connection_manager.send_message(session_id, {
                        "type": "error",
                        "message": f"Tool not found: {request.tool}"
                    })
                    continue
                
                try:
                    # Execute tool
                    result = await tool.execute(request.parameters)
                    
                    # Store tool execution in context
                    context_manager.add_message(
                        session_id,
                        "tool",
                        json.dumps({
                            "tool": request.tool,
                            "parameters": request.parameters,
                            "result": result
                        })
                    )
                    
                    # Send result
                    await connection_manager.send_message(session_id, {
                        "type": "tool_result",
                        "tool": request.tool,
                        "result": result
                    })
                
                except Exception as e:
                    await connection_manager.send_message(session_id, {
                        "type": "error",
                        "message": f"Tool execution failed: {str(e)}"
                    })

            elif request.type == "list_tools":
                # List available tools
                tools = tool_registry.list_tools()
                await connection_manager.send_message(session_id, {
                    "type": "tools_list",
                    "tools": tools
                })

            else:
                await connection_manager.send_message(session_id, {
                    "type": "error",
                    "message": f"Unknown request type: {request.type}"
                })

    except WebSocketDisconnect:
        connection_manager.disconnect(session_id)
        # Optionally clear context or keep for reconnection
        # context_manager.clear_context(session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)