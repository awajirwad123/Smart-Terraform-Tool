"""Intelligent Validator for Terraform code"""
from typing import Dict, List, Optional, Any
import json
from ..base import LLMComponentBase

class IntelligentValidator(LLMComponentBase):
    """
    Intelligent Validator for analyzing and improving Terraform code.
    
    This component handles:
    1. Error Analysis & Fixes: Identify and fix issues in Terraform code
    2. Best Practice Checking: Ensure code follows best practices
    3. Security Recommendations: Check for security issues and recommend fixes
    """
    
    def __init__(self, deployment_id: Optional[str] = None):
        """Initialize the Intelligent Validator component"""
        super().__init__("validator", deployment_id)
        
        # Register some mock responses for testing when Azure OpenAI is not available
        self._register_default_mocks()
    
    async def validate_terraform(self, template_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate Terraform template files for errors and best practices.
        
        Args:
            template_files: Dictionary of Terraform files
            
        Returns:
            Validation results including errors, warnings, and suggestions
        """
        system_prompt = """
        As a Terraform validator, analyze the provided template files for errors, issues, and
        best practice violations. Check for:
        
        1. Syntax errors
        2. Semantic errors (resource dependencies, etc.)
        3. Security issues (overly permissive policies, etc.)
        4. Best practice violations
        5. Potential bugs or edge cases
        
        Format your response as a structured JSON object with these sections:
        - errors: Array of critical issues that must be fixed
        - warnings: Array of issues that should be addressed but aren't critical
        - suggestions: Array of suggestions for improvement
        
        Each issue should include:
        - file: The filename
        - location: Line number or resource identifier
        - severity: One of "critical", "high", "medium", "low"
        - message: Description of the issue
        - recommendation: How to fix the issue
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=template_files,
            json_response=True,
            temperature=0.1,
            mock_response_key="validate_terraform"
        )
            
    async def suggest_fixes(self, template_files: Dict[str, str], validation_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Suggest fixes for issues identified in validation.
        
        Args:
            template_files: Dictionary of Terraform files
            validation_results: Validation results from validate_terraform
            
        Returns:
            Updated template files with fixes
        """
        system_prompt = """
        As a Terraform expert, fix the issues identified in the validation results. 
        Modify the provided template files to:
        
        1. Fix all errors
        2. Address security concerns
        3. Implement best practices
        4. Improve code quality
        
        Return a JSON object with filenames as keys and the updated file content as values.
        Include all original files even if they weren't modified.
        Add comments before each fix explaining what was changed and why.
        """
        
        input_content = {
            "template_files": template_files,
            "validation_results": validation_results
        }
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=input_content,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="suggest_fixes"
        )
    
    async def check_best_practices(self, template_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Check template for best practice adherence and suggest improvements.
        
        Args:
            template_files: Dictionary of Terraform files
            
        Returns:
            Best practice analysis and recommendations
        """
        system_prompt = """
        As a Terraform best practices expert, analyze the provided template files and provide:
        
        1. Overall best practice score (0-100)
        2. Analysis of code structure and organization
        3. Analysis of resource naming conventions
        4. Analysis of variable use and defaults
        5. Security posture assessment
        6. Specific recommendations for improvement
        
        Format your response as a structured JSON object with the following sections:
        - score: Overall score (0-100)
        - structure: Assessment of code structure
        - naming: Assessment of naming conventions
        - variables: Assessment of variable usage
        - security: Assessment of security practices
        - recommendations: Specific improvement recommendations
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=template_files,
            json_response=True,
            temperature=0.1,
            mock_response_key="check_best_practices"
        )
    
    async def check_security(self, template_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Perform a security-focused analysis of Terraform code.
        
        Args:
            template_files: Dictionary of Terraform files
            
        Returns:
            Security analysis and recommendations
        """
        system_prompt = """
        As a cloud security expert, analyze the provided Terraform files for security issues.
        Focus on:
        
        1. Insecure configurations (open security groups, public access, etc.)
        2. Missing encryption settings
        3. Over-permissive IAM policies
        4. Logging and monitoring gaps
        5. Compliance issues (HIPAA, PCI, etc.)
        
        Format your response as a structured JSON object with the following sections:
        - findings: Array of security findings
        - compliance: Compliance assessment
        - risk_score: Overall risk score (high, medium, low)
        - recommendations: Security recommendations
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=template_files,
            json_response=True,
            temperature=0.1,
            mock_response_key="check_security"
        )
    
    def _register_default_mocks(self):
        """Register default mock responses for testing"""
        # Mock response for validating terraform
        self.register_mock_response("validate_terraform", {
            "errors": [
                {
                    "file": "main.tf",
                    "location": "aws_instance.web",
                    "severity": "critical",
                    "message": "Security group not specified for EC2 instance",
                    "recommendation": "Add security_groups attribute to aws_instance.web resource"
                }
            ],
            "warnings": [
                {
                    "file": "main.tf",
                    "location": "aws_vpc.main",
                    "severity": "medium",
                    "message": "Missing DNS support configuration",
                    "recommendation": "Add enable_dns_support and enable_dns_hostnames attributes"
                },
                {
                    "file": "variables.tf",
                    "location": "variable.ami_id",
                    "severity": "medium",
                    "message": "AMI ID hardcoded as default",
                    "recommendation": "Remove default value and require explicit ami_id input"
                }
            ],
            "suggestions": [
                {
                    "file": "main.tf",
                    "location": "general",
                    "severity": "low",
                    "message": "Missing resource tagging strategy",
                    "recommendation": "Add consistent tags to all resources including environment and owner"
                },
                {
                    "file": "outputs.tf",
                    "location": "general",
                    "severity": "low",
                    "message": "Missing descriptions for outputs",
                    "recommendation": "Add descriptive descriptions to all outputs"
                }
            ]
        })
        
        # Mock response for suggesting fixes
        self.register_mock_response("suggest_fixes", {
            "main.tf": """
provider "aws" {
  region = var.region
}

# Added DNS support as recommended
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  # Added consistent tagging as suggested
  tags = {
    Name        = var.vpc_name
    Environment = var.environment
    Owner       = "terraform"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.public_subnet_cidr
  availability_zone = "${var.region}a"
  
  # Added consistent tagging as suggested
  tags = {
    Name        = "${var.vpc_name}-public"
    Environment = var.environment
    Owner       = "terraform"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_cidr
  availability_zone = "${var.region}a"
  
  # Added consistent tagging as suggested
  tags = {
    Name        = "${var.vpc_name}-private"
    Environment = var.environment
    Owner       = "terraform"
  }
}

# Added security group for EC2 instances
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
  
  # Added consistent tagging as suggested
  tags = {
    Name        = "${var.vpc_name}-web-sg"
    Environment = var.environment
    Owner       = "terraform"
  }
}

# Fixed critical issue - added security group to instances
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]
  
  # Added consistent tagging as suggested
  tags = {
    Name        = "web-${count.index + 1}"
    Environment = var.environment
    Owner       = "terraform"
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

# Fixed issue - removed hardcoded AMI ID
variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  # No default - require explicit input
}

variable "environment" {
  description = "Deployment environment (dev, test, prod)"
  type        = string
  default     = "dev"
}
""",
            "outputs.tf": """
# Added improved descriptions as suggested
output "vpc_id" {
  description = "ID of the created VPC, use for reference in other resources"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet, use for internet-facing resources"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "ID of the private subnet, use for internal resources"
  value       = aws_subnet.private.id
}

output "instance_ids" {
  description = "IDs of the created EC2 instances, use for management and monitoring"
  value       = aws_instance.web[*].id
}

output "security_group_id" {
  description = "ID of the web security group, use for additional security rules"
  value       = aws_security_group.web_sg.id
}
"""
        })
        
        # Mock response for checking best practices
        self.register_mock_response("check_best_practices", {
            "score": 68,
            "structure": {
                "assessment": "Moderate",
                "strengths": ["Clear resource organization", "Logical file separation"],
                "weaknesses": ["Limited use of modules", "No locals for repeated values"]
            },
            "naming": {
                "assessment": "Good",
                "strengths": ["Consistent resource naming", "Descriptive variable names"],
                "weaknesses": ["No naming convention for tags"]
            },
            "variables": {
                "assessment": "Fair",
                "strengths": ["Good use of variable typing", "Appropriate defaults"],
                "weaknesses": ["Missing validation blocks", "Some hardcoded values"]
            },
            "security": {
                "assessment": "Poor",
                "strengths": ["No overly permissive IAM policies"],
                "weaknesses": ["Missing security groups", "Open ingress rules", "No encryption configured"]
            },
            "recommendations": [
                "Implement a module structure for reusable components",
                "Add variable validation blocks",
                "Implement a consistent tagging strategy",
                "Improve security group configuration",
                "Add encryption for sensitive data",
                "Use data sources for AMI lookup instead of hardcoded values"
            ]
        })
        
        # Mock response for checking security
        self.register_mock_response("check_security", {
            "findings": [
                {
                    "severity": "high",
                    "description": "Missing security group for EC2 instances",
                    "impact": "Instances could be accessible from any source",
                    "recommendation": "Add security group with restricted ingress"
                },
                {
                    "severity": "medium", 
                    "description": "Public subnet with instances directly exposed",
                    "impact": "Increased attack surface for instances",
                    "recommendation": "Use private subnets with NAT gateway or bastion host"
                },
                {
                    "severity": "medium",
                    "description": "No encryption in transit configuration",
                    "impact": "Data transmitted to/from instances could be intercepted",
                    "recommendation": "Configure TLS and ensure HTTPS usage"
                }
            ],
            "compliance": {
                "hipaa": "non_compliant",
                "pci": "non_compliant",
                "iso27001": "partially_compliant",
                "issues": [
                    "Missing encryption",
                    "Insufficient access controls",
                    "Inadequate logging"
                ]
            },
            "risk_score": "high",
            "recommendations": [
                "Implement security groups with principle of least privilege",
                "Configure encryption in transit and at rest",
                "Implement a bastion host for secure access",
                "Enable detailed CloudTrail logging",
                "Add AWS Config rules for continuous compliance monitoring"
            ]
        }) 