#!/bin/bash
# Bash script to set Azure OpenAI environment variables for local development

# Azure OpenAI Configuration
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com"
export AZURE_OPENAI_KEY="your-api-key-goes-here"
export AZURE_OPENAI_VERSION="2023-07-01-preview"

# Model Deployment IDs
export AZURE_OPENAI_PARSER_DEPLOYMENT_ID="gpt-4"
export AZURE_OPENAI_GENERATOR_DEPLOYMENT_ID="gpt-4"
export AZURE_OPENAI_VALIDATOR_DEPLOYMENT_ID="gpt-4"
export AZURE_OPENAI_OPTIMIZER_DEPLOYMENT_ID="gpt-4"

# Enable Azure OpenAI integration
export USE_AZURE_OPENAI="true"

echo "Azure OpenAI environment variables have been set for this shell session."
echo "Run the FastAPI application now with: python main.py" 