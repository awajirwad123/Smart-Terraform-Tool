"""Template Generator for Terraform code"""
from typing import Dict, List, Optional, Any
import json
from ..base import LLMComponentBase

class TemplateGenerator(LLMComponentBase):
    """
    Template Generator for creating and analyzing Terraform templates.
    
    This component handles:
    1. Code Generation & Analysis: Create Terraform code from requirements
    2. Template Customization: Modify templates to meet specific needs
    3. Documentation Generation: Create documentation for templates
    """
    
    def __init__(self, deployment_id: Optional[str] = None):
        """Initialize the Template Generator component"""
        super().__init__("generator", deployment_id)
        
        # Register some mock responses for testing when Azure OpenAI is not available
        self._register_default_mocks()
    
    async def generate_terraform_template(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate Terraform template code based on requirements.
        
        Args:
            requirements: Structured infrastructure requirements
            
        Returns:
            Dictionary of generated Terraform files
        """
        system_prompt = """
        You are an expert Terraform developer. Generate high-quality, production-ready Terraform code 
        based on the provided requirements. Follow these guidelines:
        
        1. Use modular structure with best practices
        2. Include appropriate variables and outputs
        3. Follow security best practices
        4. Add clear comments explaining purpose of resources
        5. Ensure resource naming follows conventions
        6. Include appropriate provider configuration
        
        Return a JSON object with filenames as keys and file content as values.
        Include at minimum: main.tf, variables.tf, outputs.tf
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=requirements,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="generate_template"
        )
            
    async def analyze_template(self, template_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze a Terraform template to extract key information.
        
        Args:
            template_files: Dictionary of Terraform files
            
        Returns:
            Analysis results including resources, variables, etc.
        """
        system_prompt = """
        As a Terraform code analyst, review the provided template files and provide a comprehensive 
        analysis including:
        
        1. List of resources being created
        2. Required variables and their purpose
        3. Outputs provided by the template
        4. Estimated deployment complexity
        5. Potential cost considerations
        6. Security considerations and recommendations
        
        Format your response as a structured JSON object with the following keys:
        - resources: Array of resources with types and configurations
        - variables: Array of variables with types, defaults, and descriptions
        - outputs: Array of outputs with descriptions
        - complexity: Assessment of deployment complexity
        - cost: Cost considerations
        - security: Security considerations and recommendations
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=template_files,
            json_response=True,
            mock_response_key="analyze_template"
        )
    
    async def generate_documentation(self, template_files: Dict[str, str], analysis: Dict[str, Any]) -> str:
        """
        Generate comprehensive documentation for a Terraform template.
        
        Args:
            template_files: Dictionary of Terraform files
            analysis: Analysis of the template
            
        Returns:
            Markdown documentation
        """
        system_prompt = """
        You are a technical documentation specialist. Create comprehensive Markdown documentation 
        for the Terraform template. Include:
        
        1. Overview of architecture
        2. Prerequisites
        3. Usage instructions
        4. Variable descriptions with examples
        5. Output descriptions
        6. Deployment instructions
        7. Management and maintenance guidance
        
        Format your response as Markdown text.
        """
        
        input_content = {
            "template_files": template_files,
            "analysis": analysis
        }
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=input_content,
            json_response=False,
            temperature=0.2,
            mock_response_key="generate_documentation"
        )
    
    async def customize_template(self, template_files: Dict[str, str], customizations: Dict[str, Any]) -> Dict[str, str]:
        """
        Customize an existing Terraform template based on specific requirements.
        
        Args:
            template_files: Dictionary of existing Terraform files
            customizations: Customization requirements
            
        Returns:
            Updated template files
        """
        system_prompt = """
        As a Terraform customization expert, modify the provided template files according to the
        customization requirements. Ensure that:
        
        1. All requested changes are implemented
        2. The modified code maintains best practices
        3. Code remains readable and well-documented
        4. Changes are highlighted in comments
        
        Return a JSON object with filenames as keys and the updated file content as values.
        Include all original files even if they weren't modified.
        """
        
        input_content = {
            "template_files": template_files,
            "customizations": customizations
        }
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=input_content,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="customize_template"
        )
    
    def _register_default_mocks(self):
        """Register default mock responses for testing"""
        # Mock response for generating template
        self.register_mock_response("generate_template", {
            "main.tf": """
provider "aws" {
  region = var.region
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  
  tags = {
    Name = var.vpc_name
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.public_subnet_cidr
  availability_zone = "${var.region}a"
  
  tags = {
    Name = "${var.vpc_name}-public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_cidr
  availability_zone = "${var.region}a"
  
  tags = {
    Name = "${var.vpc_name}-private"
  }
}

resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  
  tags = {
    Name = "web-${count.index + 1}"
  }
}
""",
            "variables.tf": """
variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "main-vpc"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  type        = number
  default     = 2
}

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}
""",
            "outputs.tf": """
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "ID of the private subnet"
  value       = aws_subnet.private.id
}

output "instance_ids" {
  description = "IDs of the created EC2 instances"
  value       = aws_instance.web[*].id
}
"""
        })
        
        # Mock response for analyzing template
        self.register_mock_response("analyze_template", {
            "resources": [
                {"type": "aws_vpc", "name": "main", "count": 1},
                {"type": "aws_subnet", "name": "public", "count": 1},
                {"type": "aws_subnet", "name": "private", "count": 1},
                {"type": "aws_instance", "name": "web", "count": "variable"}
            ],
            "variables": [
                {"name": "region", "type": "string", "default": "us-west-2", "description": "AWS region to deploy resources"},
                {"name": "vpc_cidr", "type": "string", "default": "10.0.0.0/16", "description": "CIDR block for the VPC"},
                # More variables...
            ],
            "outputs": [
                {"name": "vpc_id", "description": "ID of the created VPC"},
                {"name": "public_subnet_id", "description": "ID of the public subnet"},
                # More outputs...
            ],
            "complexity": {
                "level": "medium",
                "explanation": "Basic infrastructure with multiple related resources"
            },
            "cost": {
                "estimated_monthly": "$50-100",
                "main_cost_factors": ["EC2 instances", "data transfer"]
            },
            "security": {
                "concerns": ["Public subnet accessibility", "No security groups defined"],
                "recommendations": ["Add security groups", "Implement network ACLs"]
            }
        })
        
        # Mock response for generating documentation
        self.register_mock_response("generate_documentation", """
# AWS VPC with EC2 Instances

## Overview

This Terraform template deploys a basic AWS VPC architecture with public and private subnets, along with EC2 instances for a web application.

## Prerequisites

- AWS account
- Terraform v1.0+
- AWS CLI configured

## Usage

```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| region | AWS region to deploy resources | string | us-west-2 |
| vpc_cidr | CIDR block for the VPC | string | 10.0.0.0/16 |
| vpc_name | Name of the VPC | string | main-vpc |
| ... | ... | ... | ... |

## Architecture

The architecture consists of:
- A VPC with CIDR 10.0.0.0/16
- Public subnet in the first availability zone
- Private subnet in the first availability zone
- EC2 instances in the public subnet

## Maintenance

Remember to destroy resources when no longer needed:

```bash
terraform destroy
```
""")
        
        # Mock response for customizing template
        self.register_mock_response("customize_template", {
            "main.tf": """
provider "aws" {
  region = var.region
}

# Modified VPC with DNS support as requested
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  tags = {
    Name        = var.vpc_name
    Environment = var.environment
  }
}

# Added Internet Gateway as requested
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.vpc_name}-public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_cidr
  availability_zone = "${var.region}a"
  
  tags = {
    Name = "${var.vpc_name}-private"
  }
}

# Added security group as requested
resource "aws_security_group" "web_sg" {
  name        = "${var.vpc_name}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]
  
  tags = {
    Name = "web-${count.index + 1}"
    Environment = var.environment
  }
}
""",
            "variables.tf": """
variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "main-vpc"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  type        = number
  default     = 2
}

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

# Added new variable as requested
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
""",
            "outputs.tf": """
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "ID of the private subnet"
  value       = aws_subnet.private.id
}

output "instance_ids" {
  description = "IDs of the created EC2 instances"
  value       = aws_instance.web[*].id
}

# Added new output as requested
output "security_group_id" {
  description = "ID of the web security group"
  value       = aws_security_group.web_sg.id
}
"""
        }) 