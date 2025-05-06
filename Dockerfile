FROM python:3.10-slim

WORKDIR /app

# Install Terraform
RUN apt-get update && apt-get install -y curl unzip && \
    curl -fsSL https://releases.hashicorp.com/terraform/1.7.1/terraform_1.7.1_linux_amd64.zip -o terraform.zip && \
    unzip terraform.zip -d /usr/local/bin && \
    rm terraform.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "mcp[cli]"

# Copy the rest of the application
COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# Expose the port for MCP Server
EXPOSE 8001

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV API_BASE_URL=http://localhost:8000
ENV MCP_PORT=8001

# Create a script to run both servers
RUN echo '#!/bin/sh\n\
echo "Starting FastAPI server..."\n\
uvicorn main:app --host 0.0.0.0 --port 8000 & \n\
FASTAPI_PID=$!\n\
echo "FastAPI server started with PID: $FASTAPI_PID"\n\
sleep 3\n\
echo "Starting MCP server..."\n\
python mcp_server.py --host 0.0.0.0 --port $MCP_PORT & \n\
MCP_PID=$!\n\
echo "MCP server started with PID: $MCP_PID"\n\
wait $FASTAPI_PID $MCP_PID' > /app/start.sh && chmod +x /app/start.sh

# Run the application with both servers
CMD ["/app/start.sh"] 