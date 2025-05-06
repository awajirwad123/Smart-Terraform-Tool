from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
import json
import httpx
import os
import logging
import argparse
import sys

from mcp.server.fastmcp import FastMCP, Context, Image


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


mcp = FastMCP(
    "Terraform MCP Server", 
    description="Terraform Management Control Plane with LLM enhancements",
    dependencies=["fastapi", "sqlalchemy", "terraform"]
)


class TerraformAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        logger.info(f"Initializing TerraformAPI with base URL: {base_url}")
        self.client = httpx.AsyncClient(base_url=base_url)
    
    async def list_templates(self, provider=None, tag=None):
        params = {}
        if provider:
            params["provider"] = provider
        if tag:
            params["tag"] = tag
        logger.info(f"Calling list_templates with params: {params}")
        try:
            response = await self.client.get("/api/templates/", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling list_templates: {str(e)}")
            return {"error": str(e)}
    
    async def get_template(self, template_id):
        logger.info(f"Calling get_template with template_id: {template_id}")
        try:
            response = await self.client.get(f"/api/templates/{template_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling get_template: {str(e)}")
            return {"error": str(e)}
    
    async def get_template_files(self, template_id):
        logger.info(f"Calling get_template_files with template_id: {template_id}")
        try:
            response = await self.client.get(f"/api/templates/{template_id}/files")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling get_template_files: {str(e)}")
            return {"error": str(e)}
    
    async def get_template_file_content(self, template_id, file_path):
        logger.info(f"Calling get_template_file_content with template_id: {template_id}, file_path: {file_path}")
        try:
            response = await self.client.get(f"/api/templates/{template_id}/files/{file_path}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling get_template_file_content: {str(e)}")
            return {"error": str(e)}
    
    async def execute_terraform(self, template_id, variables, workspace="default"):
        payload = {
            "template_id": template_id,
            "variables": variables,
            "workspace": workspace
        }
        logger.info(f"Calling execute_terraform with payload: {payload}")
        try:
            response = await self.client.post("/api/terraform/execute", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling execute_terraform: {str(e)}")
            return {"error": str(e)}
    
    async def get_job_status(self, job_id):
        logger.info(f"Calling get_job_status with job_id: {job_id}")
        try:
            response = await self.client.get(f"/api/terraform/job/{job_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling get_job_status: {str(e)}")
            return {"error": str(e)}
    
    async def get_job_logs(self, job_id):
        logger.info(f"Calling get_job_logs with job_id: {job_id}")
        try:
            response = await self.client.get(f"/api/terraform/job/{job_id}/logs")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling get_job_logs: {str(e)}")
            return {"error": str(e)}
    
    async def validate_terraform(self, template_id=None, template_content=None, variables=None, scan_types=None):
        payload = {}
        if template_id:
            payload["template_id"] = template_id
        if template_content:
            payload["template_content"] = template_content
        if variables:
            payload["variables"] = variables
        if scan_types:
            payload["scan_types"] = scan_types
        
        logger.info(f"Calling validate_terraform with payload: {payload}")
        try:
            response = await self.client.post("/api/validation/terraform", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling validate_terraform: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        logger.info("Closing TerraformAPI client")
        await self.client.aclose()


@dataclass
class AppContext:
    api: TerraformAPI


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # In Docker, we need to use the service name as the hostname
    # When running locally, we use localhost
    # The API_BASE_URL environment variable allows overriding this
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:8000")
    
    # If in Docker, use the app service name
    if os.path.exists("/.dockerenv"):
        logger.info("Running in Docker environment")
        api_base_url = "http://fastapi:8000"
    
    logger.info(f"Using API base URL: {api_base_url}")
    api = TerraformAPI(base_url=api_base_url)
    
    try:
        yield AppContext(api=api)
    finally:
        # Clean up connections
        await api.close()


# Pass lifespan to server
mcp = FastMCP("Terraform MCP Server", lifespan=app_lifespan)


# Expose templates as resources - use only URI parameters in function signature
@mcp.resource("templates://list/{provider}")
async def list_templates_resource(provider):
    """List available Terraform templates for a specific provider"""
    # ctx is implicitly provided by the framework
    ctx = list_templates_resource.current_context
    api = ctx.request_context.lifespan_context.api
    templates = await api.list_templates(provider=provider)
    return json.dumps(templates, indent=2)


@mcp.resource("template://{template_id}")
async def get_template_resource(template_id):
    """Get details of a specific Terraform template"""
    # ctx is implicitly provided by the framework
    ctx = get_template_resource.current_context
    api = ctx.request_context.lifespan_context.api
    template = await api.get_template(template_id)
    return json.dumps(template, indent=2)


@mcp.resource("template://{template_id}/files")
async def get_template_files_resource(template_id):
    """Get list of files in a Terraform template"""
    # ctx is implicitly provided by the framework
    ctx = get_template_files_resource.current_context
    api = ctx.request_context.lifespan_context.api
    files = await api.get_template_files(template_id)
    return json.dumps(files, indent=2)


@mcp.resource("template://{template_id}/file/{file_path}")
async def get_template_file_content_resource(template_id, file_path):
    """Get content of a specific file in a Terraform template"""
    # ctx is implicitly provided by the framework
    ctx = get_template_file_content_resource.current_context
    api = ctx.request_context.lifespan_context.api
    file_content = await api.get_template_file_content(template_id, file_path)
    return file_content.get("content", "")


# Define tools for Terraform operations
@mcp.tool()
async def list_templates(ctx: Context, provider: str = None, tag: str = None) -> str:
    """
    List available Terraform templates
    
    Args:
        provider: Filter templates by cloud provider (e.g., aws, azure)
        tag: Filter templates by tag (e.g., networking, security)
    """
    api = ctx.request_context.lifespan_context.api
    templates = await api.list_templates(provider=provider, tag=tag)
    return json.dumps(templates, indent=2)


@mcp.tool()
async def execute_terraform(
    ctx: Context,
    template_id: str, 
    variables: dict, 
    workspace: str = "default"
) -> str:
    """
    Execute a Terraform template with provided variables
    
    Args:
        template_id: ID of the template to execute
        variables: Dictionary of variables for the template
        workspace: Terraform workspace name (default is "default")
    """
    api = ctx.request_context.lifespan_context.api
    result = await api.execute_terraform(template_id, variables, workspace)
    
    # Track the job status
    job_id = result.get("job_id")
    ctx.info(f"Terraform execution started with job ID: {job_id}")
    
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_job_status(ctx: Context, job_id: str) -> str:
    """
    Get the status of a Terraform execution job
    
    Args:
        job_id: ID of the job to check
    """
    api = ctx.request_context.lifespan_context.api
    status = await api.get_job_status(job_id)
    return json.dumps(status, indent=2)


@mcp.tool()
async def get_job_logs(ctx: Context, job_id: str) -> str:
    """
    Get logs from a Terraform execution job
    
    Args:
        job_id: ID of the job to get logs for
    """
    api = ctx.request_context.lifespan_context.api
    logs = await api.get_job_logs(job_id)
    return json.dumps(logs, indent=2)


@mcp.tool()
async def validate_terraform(
    ctx: Context,
    template_id: str = None,
    template_content: dict = None,
    variables: dict = None, 
    scan_types: list = None
) -> str:
    """
    Validate Terraform templates for syntax, security, cost, and best practices
    
    Args:
        template_id: ID of the template to validate
        template_content: Dictionary of file contents if no template_id provided
        variables: Dictionary of variables for validation
        scan_types: List of scan types to perform (syntax, security, cost, best_practices)
    """
    api = ctx.request_context.lifespan_context.api
    validation = await api.validate_terraform(template_id, template_content, variables, scan_types)
    return json.dumps(validation, indent=2)


# Define prompts for common operations
@mcp.prompt()
def create_infrastructure(provider: str, description: str) -> str:
    """
    Prompt to help create infrastructure based on requirements
    
    Args:
        provider: Cloud provider (aws, azure, gcp)
        description: Description of the infrastructure needed
    """
    return f"""
    I need to create infrastructure on {provider} with these requirements:
    
    {description}
    
    Please help me:
    1. Find appropriate templates
    2. Understand the required variables
    3. Execute the correct template with proper variables
    4. Validate the infrastructure for security and best practices
    """


@mcp.prompt()
def troubleshoot_deploy(job_id: str, error_message: str) -> str:
    """
    Prompt to help troubleshoot Terraform deployment errors
    
    Args:
        job_id: The Terraform job ID that failed
        error_message: The error message or description of the issue
    """
    return f"""
    I'm having trouble with my Terraform deployment (job ID: {job_id}).
    
    The error message is:
    {error_message}
    
    Please help me:
    1. Understand what's causing this error
    2. Suggest possible solutions
    3. Provide code or configuration changes to fix the issue
    """


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Terraform MCP Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to bind to")
    return parser.parse_args()


# Main execution
if __name__ == "__main__":
    args = parse_args()
    logger.info(f"Starting MCP server on {args.host}:{args.port}")
    
    # FastMCP.run() doesn't accept host/port parameters directly
    mcp.run() 