# MCP FastAPI Server

A Terraform MCP (Management Control Plane) Server with LLM Enhancement capabilities.

## Features

- API Layer with versioned endpoints
- Advanced Terraform template validation
- Job management and execution
- Template management
- LLM Integration through MCP (Model Context Protocol)
- Integration points for LLM enhancements

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Docker & Docker Compose (for containerized deployment)
- Terraform 1.0+ (included in Docker image)
- Claude Desktop (optional, for LLM integration)

### Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server

Start the development server:

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at http://localhost:8000

### API Documentation

Once the server is running, you can access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Deployment

To run the server using Docker:

```bash
docker-compose up --build
```

This will start both the FastAPI server on port 8000 and the MCP server on port 8001.

### Claude Desktop Integration

You can integrate the MCP server with Claude Desktop for a more interactive LLM experience:

```bash
# Install the MCP server into Claude Desktop
python install_claude.py
```

This requires Claude Desktop to be installed on your system.

## Architecture

The MCP FastAPI Server follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Validation Layer**: Validates Terraform templates
3. **Execution Layer**: Executes Terraform operations
4. **Storage Layer**: Manages templates and state
5. **MCP Layer**: Integrates with LLMs through Model Context Protocol

### MCP Integration

The MCP server exposes the following capabilities to LLMs:

- **Resources**: Templates, template files, and template content
- **Tools**: Execute Terraform, validate templates, monitor jobs
- **Prompts**: Infrastructure creation, deployment troubleshooting

## Development

### Project Structure

```
mcp-server/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── terraform.py
│   │   │   │   ├── jobs.py
│   │   │   │   ├── templates.py
│   │   │   │   └── validation.py
│   │   │   └── __init__.py
│   │   ├── router.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── init_db.py
│   ├── schemas/
│   │   ├── job.py
│   │   └── template.py
│   └── __init__.py
├── main.py
├── mcp_server.py
├── install_claude.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## License

[MIT](LICENSE) 