# MCP Server Demo

This project demonstrates the implementation of a Model Context Protocol (MCP) server. MCP is a protocol designed to facilitate communication between AI models and external tools/services while maintaining context awareness.

## Features

- Basic MCP server implementation
- Example tool integrations
- Context management demonstration
- WebSocket-based real-time communication
- Simple client example

## Project Structure

```
mcp-server-demo/
├── src/
│   ├── server.py           # Main MCP server implementation
│   ├── tools/              # Tool implementations
│   │   ├── __init__.py
│   │   └── basic_tools.py
│   ├── context/            # Context management
│   │   ├── __init__.py
│   │   └── manager.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── examples/              # Example usage
│   ├── client.py
│   └── tools_demo.py
├── tests/                # Test cases
│   └── test_server.py
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tian1ll1/mcp-server-demo.git
cd mcp-server-demo
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the MCP server:
```bash
python src/server.py
```

2. Run the example client:
```bash
python examples/client.py
```

## How It Works

The MCP server implements the following key components:

1. **Context Management**: Maintains conversation history and relevant context for each session.
2. **Tool Registry**: Manages available tools and their specifications.
3. **Message Processing**: Handles incoming messages and routes them to appropriate tools.
4. **WebSocket Server**: Provides real-time communication with clients.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.