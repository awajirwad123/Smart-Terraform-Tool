# PowerShell script to set Azure OpenAI environment variables for local development

# Azure OpenAI Configuration
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com"
$env:AZURE_OPENAI_KEY="your-api-key-goes-here"
$env:AZURE_OPENAI_VERSION="2023-07-01-preview"

# Model Deployment IDs
$env:AZURE_OPENAI_PARSER_DEPLOYMENT_ID="gpt-4"
$env:AZURE_OPENAI_GENERATOR_DEPLOYMENT_ID="gpt-4"
$env:AZURE_OPENAI_VALIDATOR_DEPLOYMENT_ID="gpt-4"
$env:AZURE_OPENAI_OPTIMIZER_DEPLOYMENT_ID="gpt-4"

# Enable Azure OpenAI integration
$env:USE_AZURE_OPENAI="true"

Write-Host "Azure OpenAI environment variables have been set for this PowerShell session."
Write-Host "Run the FastAPI application now with: python main.py" 