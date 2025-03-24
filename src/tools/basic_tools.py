from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class Tool(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter]
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        raise NotImplementedError

class EchoTool(Tool):
    def __init__(self):
        super().__init__(
            name="echo",
            description="Echoes back the input message",
            parameters=[
                ToolParameter(
                    name="message",
                    type="string",
                    description="Message to echo back"
                )
            ]
        )
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"message": params["message"]}

class TimeTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_time",
            description="Returns the current time",
            parameters=[]
        )
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"time": datetime.now().isoformat()}

class CalculatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="calculate",
            description="Performs basic arithmetic operations",
            parameters=[
                ToolParameter(
                    name="operation",
                    type="string",
                    description="Operation to perform (add, subtract, multiply, divide)"
                ),
                ToolParameter(
                    name="a",
                    type="number",
                    description="First number"
                ),
                ToolParameter(
                    name="b",
                    type="number",
                    description="Second number"
                )
            ]
        )
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        operation = params["operation"]
        a = float(params["a"])
        b = float(params["b"])
        
        result = None
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            result = a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        return {"result": result}

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        
        # Register default tools
        self.register_tool(EchoTool())
        self.register_tool(TimeTool())
        self.register_tool(CalculatorTool())
    
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool."""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": [param.dict() for param in tool.parameters]
            }
            for tool in self.tools.values()
        ]