#!/usr/bin/env python
"""
A helper script to install the Terraform MCP server into Claude Desktop.
"""

import sys
import os
import subprocess

def main():
    """Install the Terraform MCP server into Claude Desktop."""
    # Check if MCP is installed
    try:
        subprocess.run(["mcp", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("MCP CLI not found. Please install with 'pip install \"mcp[cli]\"'")
        sys.exit(1)
    
    # Get the absolute path to the mcp_server.py file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "mcp_server.py")
    
    # Make sure mcp_server.py exists
    if not os.path.exists(server_path):
        print(f"Error: {server_path} does not exist.")
        sys.exit(1)
    
    # Install the server to Claude
    print("Installing Terraform MCP Server to Claude Desktop...")
    try:
        subprocess.run(
            [
                "mcp", 
                "install", 
                server_path, 
                "--name", 
                "Terraform MCP Server"
            ], 
            check=True
        )
        print("Installation successful! You can now use the Terraform MCP Server in Claude Desktop.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 