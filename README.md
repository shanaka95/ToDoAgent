# To Do Agent

A simple todo agent demo with context-aware chat interface.

## Features

- **Context Awareness**: Understands conversation history and references
- **Natural Language**: Chat-based task management
- **In-Memory Storage**: Simple demo implementation

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Run the service:
```bash
uvicorn to_do_agent.app:app --reload --port 8000
```

## Usage

### Chat Examples
```bash
# Create tasks
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "buy biscuit"}'

# Add to context
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "also eggs"}'

# List tasks
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "show my tasks"}'
```

### Context Awareness
- "buy biscuit" → creates "buy biscuit"
- "also eggs" → creates "buy eggs" (from shopping context)
- "clean kitchen" → creates "clean kitchen"
- "also bathroom" → creates "clean bathroom" (from cleaning context)

## API

- `POST /api/v1/chat` - Chat with the agent
- `GET /health` - Health check
