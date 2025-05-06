# LLM Enhancement Layer Testing Guide

This guide provides instructions and sample payloads for testing all endpoints in the LLM Enhancement Layer.

## Prerequisites

1. The FastAPI server is running on port 8000 (default)
2. Azure OpenAI credentials are properly configured in:
   - Docker Compose environment variables
   - Or using the `setup_env.ps1` (Windows) or `setup_env.sh` (Linux/macOS) scripts

## Common Testing Methods

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/llm/<endpoint>" \
  -H "Content-Type: application/json" \
  -d '<payload>'
```

### Using Python Requests

```python
import requests
import json

url = "http://localhost:8000/api/llm/<endpoint>"
payload = {...}  # Your payload as a Python dictionary
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## 1. Natural Language Parser

### 1.1 Parse Infrastructure Requirements

**Endpoint:** `/api/llm/parser/parse`

**Sample Payload:**
```json
{
  "text": "I need a high-availability web application in AWS with a load balancer, 3 EC2 instances, and an RDS database. Make sure it's properly secured with appropriate security groups and encryption for sensitive data."
}
```

**Expected Response:**
```json
{
  "provider": "aws",
  "resources": [
    {
      "type": "vpc",
      "name": "main-vpc",
      "cidr": "10.0.0.0/16"
    },
    {
      "type": "subnet",
      "name": "public-subnet",
      "cidr": "10.0.1.0/24"
    },
    {
      "type": "ec2",
      "name": "web-server",
      "instance_type": "t3.medium",
      "count": 3
    },
    {
      "type": "rds",
      "name": "database",
      "instance_type": "db.t3.medium",
      "engine": "mysql"
    },
    {
      "type": "elb",
      "name": "load-balancer"
    }
  ],
  "relationships": [
    {"source": "web-server", "target": "public-subnet", "type": "deployed_in"},
    {"source": "load-balancer", "target": "web-server", "type": "routes_to"}
  ],
  "security": {
    "encryption": "required",
    "access_controls": ["security_groups", "restrict_ssh_access"]
  },
  "constraints": {
    "availability": "high"
  },
  "metadata": {
    "purpose": "Web application hosting"
  }
}
```

### 1.2 Extract Context

**Endpoint:** `/api/llm/parser/context`

**Sample Payload:**
```json
{
  "text": "We need to deploy this infrastructure for our new e-commerce project. It should be in production and preferably in the US East region for compliance reasons. We're on a tight budget and need to launch by next month.",
  "existing_resources": {
    "vpc": {"id": "vpc-123456", "cidr": "10.0.0.0/16"},
    "subnets": [{"id": "subnet-123456", "cidr": "10.0.1.0/24"}]
  }
}
```

**Expected Response:**
```json
{
  "environment": "prod",
  "region": "us-east-1",
  "project": "e-commerce",
  "timeline": "1 month",
  "integration": ["existing_vpc", "existing_subnets"],
  "objectives": ["cost_efficient", "compliance"],
  "implicit_needs": ["security", "scalability"]
}
```

## 2. Template Generator

### 2.1 Generate Terraform Template

**Endpoint:** `/api/llm/generator/terraform`

**Sample Payload:**
```json
{
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
    ],
    "security": {
      "encryption": "required"
    }
  }
}
```

**Expected Response:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  root_block_device {\n    encrypted = true\n  }\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}",
    "variables.tf": "variable \"region\" {\n  description = \"AWS region to deploy resources\"\n  default = \"us-west-2\"\n}\n\nvariable \"ami_id\" {\n  description = \"AMI ID for EC2 instances\"\n}",
    "outputs.tf": "output \"vpc_id\" {\n  value = aws_vpc.main-vpc.id\n}\n\noutput \"instance_ids\" {\n  value = aws_instance.web-server[*].id\n}"
  }
}
```

### 2.2 Analyze Template

**Endpoint:** `/api/llm/generator/analyze`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  root_block_device {\n    encrypted = true\n  }\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}",
    "variables.tf": "variable \"region\" {\n  description = \"AWS region to deploy resources\"\n  default = \"us-west-2\"\n}\n\nvariable \"ami_id\" {\n  description = \"AMI ID for EC2 instances\"\n}"
  }
}
```

**Expected Response:**
```json
{
  "resources": [
    {"type": "aws_vpc", "name": "main-vpc", "count": 1},
    {"type": "aws_instance", "name": "web-server", "count": 2}
  ],
  "variables": [
    {"name": "region", "type": "string", "default": "us-west-2"},
    {"name": "ami_id", "type": "string", "required": true}
  ],
  "outputs": [],
  "complexity": {"level": "low", "score": 3},
  "cost": {"estimated": "medium", "resources": ["aws_instance"]},
  "security": {"level": "medium", "features": ["root_block_device_encryption"]}
}
```

### 2.3 Generate Documentation

**Endpoint:** `/api/llm/generator/documentation`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  root_block_device {\n    encrypted = true\n  }\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

**Expected Response:**
```json
{
  "documentation": "# AWS Infrastructure Documentation\n\n## Overview\n\nThis Terraform configuration deploys a basic AWS infrastructure with a VPC and EC2 instances.\n\n## Resources\n\n### VPC\n- Name: main-vpc\n- CIDR: 10.0.0.0/16\n\n### EC2 Instances\n- Name: web-server-[0-1]\n- Type: t3.medium\n- Count: 2\n- Security: Root volume encryption enabled\n\n## Variables\n\n| Name | Description | Type | Default | Required |\n|------|-------------|------|---------|:--------:|\n| region | AWS region to deploy resources | string | us-west-2 | no |\n| ami_id | AMI ID for EC2 instances | string | - | yes |\n\n## Usage\n\n```bash\nterraform init\nterraform plan -var=\"ami_id=ami-12345678\"\nterraform apply -var=\"ami_id=ami-12345678\"\n```"
}
```

### 2.4 Customize Template

**Endpoint:** `/api/llm/generator/customize`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  },
  "customizations": {
    "add_resources": ["load_balancer"],
    "modify_resources": {
      "aws_instance.web-server": {
        "instance_type": "t3.large",
        "count": 3
      }
    },
    "add_tags": {
      "Environment": "Production",
      "Project": "E-Commerce"
    }
  }
}
```

**Expected Response:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n    Environment = \"Production\"\n    Project = \"E-Commerce\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 3\n  ami = var.ami_id\n  instance_type = \"t3.large\"\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n    Environment = \"Production\"\n    Project = \"E-Commerce\"\n  }\n}\n\nresource \"aws_lb\" \"load_balancer\" {\n  name = \"web-lb\"\n  internal = false\n  load_balancer_type = \"application\"\n  subnets = var.public_subnets\n  \n  tags = {\n    Name = \"web-load-balancer\"\n    Environment = \"Production\"\n    Project = \"E-Commerce\"\n  }\n}"
  }
}
```

## 3. Intelligent Validator

### 3.1 Validate Terraform

**Endpoint:** `/api/llm/validator/validate`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

**Expected Response:**
```json
{
  "errors": [
    {
      "resource": "aws_instance.web-server",
      "property": "vpc_security_group_ids",
      "message": "Referenced security group 'aws_security_group.web_sg' is not defined",
      "severity": "error",
      "line": 14
    }
  ],
  "warnings": [
    {
      "resource": "aws_instance.web-server",
      "property": "root_block_device",
      "message": "No encryption specified for root block device",
      "severity": "warning",
      "line": 10
    }
  ],
  "suggestions": [
    {
      "resource": "aws_vpc.main-vpc",
      "property": "enable_dns_support",
      "message": "Consider enabling DNS support for the VPC",
      "severity": "info",
      "line": 5
    }
  ]
}
```

### 3.2 Suggest Fixes

**Endpoint:** `/api/llm/validator/suggest-fixes`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  },
  "validation_results": {
    "errors": [
      {
        "resource": "aws_instance.web-server",
        "property": "vpc_security_group_ids",
        "message": "Referenced security group 'aws_security_group.web_sg' is not defined",
        "severity": "error",
        "line": 14
      }
    ]
  }
}
```

**Expected Response:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_security_group\" \"web_sg\" {\n  name        = \"web-sg\"\n  description = \"Security group for web servers\"\n  vpc_id      = aws_vpc.main-vpc.id\n\n  ingress {\n    from_port   = 80\n    to_port     = 80\n    protocol    = \"tcp\"\n    cidr_blocks = [\"0.0.0.0/0\"]\n  }\n\n  egress {\n    from_port   = 0\n    to_port     = 0\n    protocol    = \"-1\"\n    cidr_blocks = [\"0.0.0.0/0\"]\n  }\n\n  tags = {\n    Name = \"web-sg\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

### 3.3 Check Best Practices

**Endpoint:** `/api/llm/validator/best-practices`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

**Expected Response:**
```json
{
  "score": 70,
  "structure": {
    "assessment": "Good separation of resources",
    "findings": ["Missing variables file", "Missing outputs"]
  },
  "naming": {
    "assessment": "Consistent naming convention",
    "findings": []
  },
  "variables": {
    "assessment": "Using variable references properly",
    "findings": ["AMI ID should have validation rules"]
  },
  "security": {
    "assessment": "Basic security measures present",
    "findings": ["Missing encryption for storage", "Security group not defined"]
  },
  "recommendations": [
    "Add variable validation for AMI ID",
    "Separate resources into multiple files",
    "Add encryption for storage volumes",
    "Define the referenced security group"
  ]
}
```

### 3.4 Check Security

**Endpoint:** `/api/llm/validator/security`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_vpc\" \"main-vpc\" {\n  cidr_block = \"10.0.0.0/16\"\n  tags = {\n    Name = \"main-vpc\"\n  }\n}\n\nresource \"aws_instance\" \"web-server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  vpc_security_group_ids = [aws_security_group.web_sg.id]\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

**Expected Response:**
```json
{
  "findings": [
    {
      "severity": "high",
      "category": "missing_resource",
      "description": "Security group 'web_sg' is referenced but not defined",
      "recommendation": "Define the security group with proper ingress/egress rules"
    },
    {
      "severity": "medium",
      "category": "encryption",
      "description": "No encryption specified for EC2 instance volumes",
      "recommendation": "Add encryption for all storage volumes"
    },
    {
      "severity": "low",
      "category": "network",
      "description": "VPC has no network ACLs defined",
      "recommendation": "Consider adding network ACLs for additional security"
    }
  ],
  "compliance": {
    "status": "failed",
    "standards": [
      {"name": "CIS AWS Foundations", "compliant": false},
      {"name": "AWS Well-Architected Framework", "compliant": false}
    ]
  },
  "risk_score": "high",
  "recommendations": [
    "Define security groups with least privilege access",
    "Implement encryption for all data at rest",
    "Add network ACLs to control traffic at the subnet level",
    "Implement IAM roles for EC2 instances instead of access keys"
  ]
}
```

## 4. Resource Optimizer

### 4.1 Optimize Cost

**Endpoint:** `/api/llm/optimizer/cost`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"app_server\" {\n  count = 3\n  ami = var.ami_id\n  instance_type = \"m5.xlarge\"\n  ebs_optimized = true\n  \n  root_block_device {\n    volume_size = 100\n    volume_type = \"gp2\"\n  }\n  \n  tags = {\n    Name = \"app-server-${count.index}\"\n  }\n}"
  },
  "budget_constraint": 500
}
```

**Expected Response:**
```json
{
  "current_estimated_cost": 750.0,
  "optimized_estimated_cost": 320.0,
  "savings_percentage": 57.3,
  "recommendations": [
    {
      "resource": "aws_instance.app_server",
      "current": "m5.xlarge",
      "recommended": "t3.large",
      "rationale": "Rightsizing for typical application workloads",
      "savings": 240.0
    },
    {
      "resource": "aws_instance.app_server.root_block_device",
      "current": "100GB gp2",
      "recommended": "50GB gp3",
      "rationale": "Reduced size and newer more cost-effective volume type",
      "savings": 90.0
    },
    {
      "resource": "aws_instance.app_server",
      "current": "On-Demand",
      "recommended": "Reserved Instance (1 year)",
      "rationale": "Commitment discount for stable workloads",
      "savings": 100.0
    }
  ],
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"app_server\" {\n  count = 3\n  ami = var.ami_id\n  instance_type = \"t3.large\"\n  ebs_optimized = true\n  \n  root_block_device {\n    volume_size = 50\n    volume_type = \"gp3\"\n  }\n  \n  tags = {\n    Name = \"app-server-${count.index}\"\n  }\n}"
  }
}
```

### 4.2 Optimize Performance

**Endpoint:** `/api/llm/optimizer/performance`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"web_server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"t3.medium\"\n  \n  root_block_device {\n    volume_type = \"gp2\"\n    volume_size = 20\n  }\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  },
  "performance_targets": {
    "throughput": "high",
    "response_time": "low"
  }
}
```

**Expected Response:**
```json
{
  "current_performance_assessment": {
    "compute": {"rating": "medium", "bottlenecks": ["cpu_contention"]},
    "storage": {"rating": "low", "bottlenecks": ["iops_limited"]},
    "network": {"rating": "medium", "bottlenecks": []}
  },
  "optimized_performance_assessment": {
    "compute": {"rating": "high", "bottlenecks": []},
    "storage": {"rating": "high", "bottlenecks": []},
    "network": {"rating": "high", "bottlenecks": []}
  },
  "improvement_summary": "Performance optimization focused on compute power and storage IOPS to handle high throughput and reduce response times",
  "recommendations": [
    {
      "resource": "aws_instance.web_server",
      "property": "instance_type",
      "current": "t3.medium",
      "recommended": "c5.large",
      "rationale": "Higher CPU performance for web serving workloads"
    },
    {
      "resource": "aws_instance.web_server.root_block_device",
      "property": "volume_type",
      "current": "gp2",
      "recommended": "gp3",
      "rationale": "Higher baseline performance and configurable IOPS"
    },
    {
      "resource": "aws_instance.web_server.root_block_device",
      "property": "iops",
      "current": "null",
      "recommended": "3000",
      "rationale": "Increased IOPS for better I/O performance"
    }
  ],
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"web_server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"c5.large\"\n  \n  root_block_device {\n    volume_type = \"gp3\"\n    volume_size = 20\n    iops = 3000\n  }\n  \n  tags = {\n    Name = \"web-server-${count.index}\"\n  }\n}"
  }
}
```

### 4.3 Suggest Architecture

**Endpoint:** `/api/llm/optimizer/architecture`

**Sample Payload:**
```json
{
  "requirements": {
    "application_type": "web",
    "load": "variable",
    "scaling": "auto",
    "availability": "high",
    "data_storage": "relational",
    "security": "high"
  }
}
```

**Expected Response:**
```json
{
  "architecture_overview": "Three-tier architecture with auto-scaling web layer, application layer, and managed database",
  "components": [
    {
      "name": "VPC",
      "type": "network",
      "description": "Isolated network with public and private subnets across multiple availability zones"
    },
    {
      "name": "Web Tier",
      "type": "compute",
      "description": "Auto-scaling group of web servers in public subnets behind an application load balancer"
    },
    {
      "name": "Application Tier",
      "type": "compute",
      "description": "Auto-scaling group of application servers in private subnets"
    },
    {
      "name": "Database Tier",
      "type": "database",
      "description": "RDS Aurora cluster with primary and replica instances across availability zones"
    },
    {
      "name": "Caching Layer",
      "type": "cache",
      "description": "ElastiCache Redis cluster for session management and data caching"
    }
  ],
  "communication": "The ALB routes traffic to the web tier, which communicates with the application tier. The application tier accesses the database and cache.",
  "scalability": "Auto-scaling groups for web and application tiers based on CPU utilization and request count metrics",
  "security": "Network segmentation with security groups, WAF for the load balancer, encryption in transit and at rest",
  "cost": "Pay-as-you-go model with potential cost optimization using reserved instances for baseline capacity",
  "diagram": "```\n[Internet] --> [WAF] --> [ALB] --> [Web Tier ASG] --> [Application Tier ASG] --> [Aurora Cluster]\n                                                  |\n                                                  v\n                                            [ElastiCache]\n```",
  "terraform_example": "module \"vpc\" {\n  source = \"terraform-aws-modules/vpc/aws\"\n  # Configuration\n}\n\nmodule \"web_tier\" {\n  source = \"terraform-aws-modules/autoscaling/aws\"\n  # Configuration\n}\n\nmodule \"app_tier\" {\n  source = \"terraform-aws-modules/autoscaling/aws\"\n  # Configuration\n}\n\nmodule \"db\" {\n  source = \"terraform-aws-modules/rds-aurora/aws\"\n  # Configuration\n}"
}
```

### 4.4 Right-Size Resources

**Endpoint:** `/api/llm/optimizer/right-size`

**Sample Payload:**
```json
{
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"api_server\" {\n  count = 4\n  ami = var.ami_id\n  instance_type = \"m5.2xlarge\"\n  \n  tags = {\n    Name = \"api-server-${count.index}\"\n  }\n}"
  },
  "utilization_data": {
    "api_server": {
      "cpu_utilization": {
        "average": 20.5,
        "peak": 45.0
      },
      "memory_utilization": {
        "average": 35.2,
        "peak": 60.0
      },
      "network_utilization": {
        "average": 15.0,
        "peak": 40.0
      }
    }
  }
}
```

**Expected Response:**
```json
{
  "current_resources": {
    "api_server": {
      "count": 4,
      "type": "m5.2xlarge",
      "vcpu": 32,
      "memory_gb": 128,
      "estimated_cost_monthly": 1200
    }
  },
  "right_sized_resources": {
    "api_server": {
      "count": 2,
      "type": "m5.xlarge",
      "vcpu": 8,
      "memory_gb": 32,
      "estimated_cost_monthly": 300
    }
  },
  "efficiency_improvement": "75% cost reduction while maintaining adequate capacity for peak loads",
  "recommendations": [
    {
      "resource": "aws_instance.api_server",
      "property": "count",
      "current": 4,
      "recommended": 2,
      "rationale": "Current CPU and memory utilization indicates over-provisioning"
    },
    {
      "resource": "aws_instance.api_server",
      "property": "instance_type",
      "current": "m5.2xlarge",
      "recommended": "m5.xlarge",
      "rationale": "Downsizing instance type to match workload requirements"
    },
    {
      "additional": "Consider adding auto-scaling for handling unexpected load increases"
    }
  ],
  "template_files": {
    "main.tf": "provider \"aws\" {\n  region = var.region\n}\n\nresource \"aws_instance\" \"api_server\" {\n  count = 2\n  ami = var.ami_id\n  instance_type = \"m5.xlarge\"\n  \n  tags = {\n    Name = \"api-server-${count.index}\"\n  }\n}"
  }
}
```

## Testing with Swagger UI

You can also use the interactive Swagger UI to test all endpoints:

1. Start the FastAPI server
2. Open http://localhost:8000/docs in your browser
3. Navigate to the "LLM Enhancement" section
4. Select an endpoint and click "Try it out"
5. Enter the sample payload and click "Execute" 