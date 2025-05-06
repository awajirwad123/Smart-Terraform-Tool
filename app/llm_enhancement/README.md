# LLM Enhancement Layer for Terraform MCP Server

The LLM Enhancement Layer adds intelligent, AI-driven capabilities to the Terraform MCP Server, leveraging Azure OpenAI services to improve the infrastructure management experience.

## Architecture

The LLM Enhancement Layer consists of four main components:

1. **Natural Language Parser**: Transforms natural language into structured infrastructure requirements
2. **Template Generator**: Creates and analyzes Terraform templates based on requirements
3. **Intelligent Validator**: Analyzes Terraform code for errors, best practices, and security issues
4. **Resource Optimizer**: Optimizes infrastructure for cost, performance, and right-sizing

## Configuration

To use the LLM Enhancement Layer with Azure OpenAI, set the following environment variables:

```
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_VERSION=2023-07-01-preview
AZURE_OPENAI_PARSER_DEPLOYMENT_ID=your-parser-model-deployment-id
AZURE_OPENAI_GENERATOR_DEPLOYMENT_ID=your-generator-model-deployment-id
AZURE_OPENAI_VALIDATOR_DEPLOYMENT_ID=your-validator-model-deployment-id
AZURE_OPENAI_OPTIMIZER_DEPLOYMENT_ID=your-optimizer-model-deployment-id
USE_AZURE_OPENAI=true
```

For testing without Azure OpenAI, set `USE_AZURE_OPENAI=false` to use mock responses.

## API Endpoints

### Natural Language Parser

- `POST /llm/parser/parse`: Parse infrastructure requirements from natural language text
- `POST /llm/parser/context`: Extract contextual information from a user request

### Template Generator

- `POST /llm/generator/terraform`: Generate Terraform template code based on requirements
- `POST /llm/generator/analyze`: Analyze a Terraform template to extract key information
- `POST /llm/generator/documentation`: Generate comprehensive documentation for a Terraform template
- `POST /llm/generator/customize`: Customize an existing Terraform template

### Intelligent Validator

- `POST /llm/validator/validate`: Validate Terraform template files for errors and best practices
- `POST /llm/validator/suggest-fixes`: Suggest fixes for issues identified in validation
- `POST /llm/validator/best-practices`: Check template for best practice adherence
- `POST /llm/validator/security`: Perform a security-focused analysis of Terraform code

### Resource Optimizer

- `POST /llm/optimizer/cost`: Optimize Terraform template for cost
- `POST /llm/optimizer/performance`: Optimize Terraform template for performance
- `POST /llm/optimizer/architecture`: Suggest optimal architecture based on requirements
- `POST /llm/optimizer/right-size`: Right-size resources based on utilization data or best practices

## Usage Examples

### Parse Natural Language to Infrastructure Requirements

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/llm/parser/parse",
    json={
        "text": "I need a highly available web application in AWS with a load balancer, 2 EC2 instances, and an RDS database"
    }
)

requirements = response.json()
print(json.dumps(requirements, indent=2))
```

### Generate Terraform Template from Requirements

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/llm/generator/terraform",
    json={
        "requirements": {
            "provider": "aws",
            "resources": [
                {
                    "type": "vpc",
                    "name": "main-vpc",
                    "cidr": "10.0.0.0/16"
                },
                {
                    "type": "ec2",
                    "name": "web-server",
                    "instance_type": "t3.medium",
                    "count": 2
                }
            ]
        }
    }
)

template_files = response.json()["template_files"]
print(json.dumps(template_files, indent=2))
```

### Validate Terraform Template

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/llm/validator/validate",
    json={
        "template_files": {
            "main.tf": "provider \"aws\" { ... }",
            "variables.tf": "variable \"region\" { ... }"
        }
    }
)

validation_results = response.json()
print(json.dumps(validation_results, indent=2))
```

### Optimize Template for Cost

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/llm/optimizer/cost",
    json={
        "template_files": {
            "main.tf": "provider \"aws\" { ... }",
            "variables.tf": "variable \"region\" { ... }"
        },
        "budget_constraint": 100.0
    }
)

optimization_results = response.json()
print(json.dumps(optimization_results, indent=2))
```

## Integration with Existing Terraform Operations

The LLM Enhancement Layer seamlessly integrates with existing Terraform operations, providing intelligent recommendations and automation while maintaining compatibility with standard Terraform workflows. 