"""Resource Optimizer for Terraform infrastructure"""
from typing import Dict, List, Optional, Any
import json
from ..base import LLMComponentBase

class ResourceOptimizer(LLMComponentBase):
    """
    Resource Optimizer for improving Terraform infrastructure.
    
    This component handles:
    1. Cost & Performance Tuning: Optimize resources for cost efficiency and performance
    2. Resource Right-sizing: Ensure resources are appropriately sized for their use case
    3. Architecture Suggestions: Provide architectural improvements
    """
    
    def __init__(self, deployment_id: Optional[str] = None):
        """Initialize the Resource Optimizer component"""
        super().__init__("optimizer", deployment_id)
        
        # Register some mock responses for testing when Azure OpenAI is not available
        self._register_default_mocks()
    
    async def optimize_cost(self, template_files: Dict[str, str], budget_constraint: Optional[float] = None) -> Dict[str, Any]:
        """
        Optimize Terraform template for cost.
        
        Args:
            template_files: Dictionary of Terraform files
            budget_constraint: Optional budget constraint in USD
            
        Returns:
            Cost optimization recommendations and modified template
        """
        system_prompt = """
        As a cloud cost optimization expert, analyze the provided Terraform template and suggest 
        optimizations to reduce cost without compromising essential functionality. Consider:
        
        1. Right-sizing resources
        2. Using reserved instances or savings plans
        3. Utilizing spot instances where appropriate
        4. Optimizing storage tiers
        5. Implementing auto-scaling
        6. Improving resource utilization
        
        Return a JSON object with the following sections:
        - current_estimated_cost: Estimated monthly cost for the current configuration
        - optimized_estimated_cost: Estimated monthly cost after optimization
        - savings_percentage: Percentage of cost reduction
        - recommendations: Array of specific recommendations
        - template_files: Modified template files with cost optimizations
        """
        
        user_content = json.dumps({
            "template_files": template_files,
            "budget_constraint": budget_constraint
        }) if budget_constraint else json.dumps({"template_files": template_files})
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=user_content,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="optimize_cost"
        )
            
    async def optimize_performance(self, template_files: Dict[str, str], performance_targets: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Optimize Terraform template for performance.
        
        Args:
            template_files: Dictionary of Terraform files
            performance_targets: Optional performance targets
            
        Returns:
            Performance optimization recommendations and modified template
        """
        system_prompt = """
        As a cloud performance optimization expert, analyze the provided Terraform template and suggest 
        optimizations to improve performance. Consider:
        
        1. Resource sizing and capabilities
        2. Network configuration and latency
        3. Distributed architecture patterns
        4. Caching strategies
        5. Database optimizations
        6. Load balancing and auto-scaling
        
        Return a JSON object with the following sections:
        - current_performance_assessment: Assessment of current performance characteristics
        - optimized_performance_assessment: Expected performance after optimization
        - improvement_summary: Summary of expected improvements
        - recommendations: Array of specific recommendations
        - template_files: Modified template files with performance optimizations
        """
        
        user_content = json.dumps({
            "template_files": template_files,
            "performance_targets": performance_targets
        }) if performance_targets else json.dumps({"template_files": template_files})
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=user_content,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="optimize_performance"
        )
    
    async def suggest_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest optimal architecture based on requirements.
        
        Args:
            requirements: Infrastructure requirements
            
        Returns:
            Architecture recommendations and diagrams
        """
        system_prompt = """
        As a cloud architect, suggest an optimal architecture based on the provided requirements.
        Your response should include:
        
        1. Overall architecture recommendation
        2. Key components and services
        3. Communication patterns
        4. Scalability approach
        5. Security considerations
        6. Cost estimates
        7. ASCII diagram representation of the architecture
        
        Return a JSON object with the following sections:
        - architecture_overview: Description of the overall architecture
        - components: Array of key components and services
        - communication: Description of communication patterns
        - scalability: Approach to scaling
        - security: Security considerations
        - cost: Cost estimates
        - diagram: ASCII diagram representation
        - terraform_example: Example Terraform snippet for a key component
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=requirements,
            json_response=True,
            temperature=0.2,
            mock_response_key="suggest_architecture"
        )
    
    async def right_size_resources(self, template_files: Dict[str, str], utilization_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Right-size resources based on utilization data or best practices.
        
        Args:
            template_files: Dictionary of Terraform files
            utilization_data: Optional utilization data for existing resources
            
        Returns:
            Right-sizing recommendations and modified template
        """
        system_prompt = """
        As a resource optimization expert, analyze the provided Terraform template and suggest 
        right-sizing optimizations. Consider:
        
        1. Instance types and sizes
        2. Storage allocations
        3. Database instance sizes
        4. Network throughput allocations
        5. Container resource limits
        
        If utilization data is provided, use it to inform your recommendations.
        Otherwise, base recommendations on best practices and typical usage patterns.
        
        Return a JSON object with the following sections:
        - current_resources: Assessment of current resource allocations
        - right_sized_resources: Recommended resource allocations
        - efficiency_improvement: Expected efficiency improvement percentage
        - recommendations: Array of specific recommendations
        - template_files: Modified template files with right-sized resources
        """
        
        user_content = json.dumps({
            "template_files": template_files,
            "utilization_data": utilization_data
        }) if utilization_data else json.dumps({"template_files": template_files})
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=user_content,
            json_response=True,
            temperature=0.2,
            max_tokens=4000,
            mock_response_key="right_size_resources"
        )
    
    def _register_default_mocks(self):
        """Register default mock responses for testing"""
        # Mock response for cost optimization
        self.register_mock_response("optimize_cost", {
            "current_estimated_cost": 342.50,
            "optimized_estimated_cost": 214.75,
            "savings_percentage": 37.3,
            "recommendations": [
                {
                    "category": "Compute",
                    "recommendation": "Switch t3.medium instances to t4g.small with ARM architecture",
                    "impact": "~$45 monthly savings",
                    "risk": "Low; requires ARM-compatible applications"
                },
                {
                    "category": "Reserved Instances",
                    "recommendation": "Purchase 1-year reserved instances for predictable workloads",
                    "impact": "~$60 monthly savings",
                    "risk": "Medium; requires 1-year commitment"
                },
                {
                    "category": "Storage",
                    "recommendation": "Move older logs to S3 Glacier Deep Archive",
                    "impact": "~$22 monthly savings",
                    "risk": "Low; reduced retrieval speed for archived logs"
                }
            ],
            "template_files": {
                "main.tf": """
provider "aws" {
  region = var.region
}

# Optimized instance type for cost savings
resource "aws_instance" "web" {
  count         = var.instance_count
  # Changed from t3.medium to t4g.small (ARM) for cost optimization
  ami           = var.arm_ami_id
  instance_type = "t4g.small"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]
  
  # Added purchase option to use Spot Instances where possible
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.012"
    }
  }
  
  tags = {
    Name = "web-${count.index + 1}"
    Environment = var.environment
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  tags = {
    Name = var.vpc_name
    Environment = var.environment
  }
}

# Remaining resources unchanged
""",
                "variables.tf": """
# Added ARM AMI variable for cost optimization
variable "arm_ami_id" {
  description = "ARM-based AMI ID for EC2 instances (for cost optimization)"
  type        = string
  default     = "ami-0123456789abcdef"
}

# Original variables retained
variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

# Remaining variables unchanged
"""
            }
        })
        
        # Mock response for performance optimization
        self.register_mock_response("optimize_performance", {
            "current_performance_assessment": {
                "compute": "Moderate; t3.medium instances with baseline performance",
                "storage": "Low; standard EBS volumes with no provisioned IOPS",
                "network": "Moderate; instances in same availability zone",
                "database": "Not present in template"
            },
            "optimized_performance_assessment": {
                "compute": "High; c5.large instances with optimized CPU performance",
                "storage": "High; EBS gp3 volumes with provisioned IOPS",
                "network": "High; enhanced networking enabled, optimized placement",
                "database": "Not applicable"
            },
            "improvement_summary": "Expected ~40% improvement in application response time, ~60% improvement in throughput",
            "recommendations": [
                {
                    "category": "Compute",
                    "recommendation": "Switch to compute-optimized c5.large instances",
                    "impact": "Improved CPU performance for web applications",
                    "cost_implication": "~15% increase in instance cost"
                },
                {
                    "category": "Storage",
                    "recommendation": "Use EBS gp3 volumes with 4000 IOPS",
                    "impact": "Faster disk I/O for applications",
                    "cost_implication": "~10% increase in storage cost"
                },
                {
                    "category": "Networking",
                    "recommendation": "Enable enhanced networking with ENA",
                    "impact": "Higher throughput, lower latency",
                    "cost_implication": "No additional cost"
                }
            ],
            "template_files": {
                "main.tf": """
provider "aws" {
  region = var.region
}

# Performance-optimized instance configuration
resource "aws_instance" "web" {
  count         = var.instance_count
  # Changed to compute-optimized instance
  ami           = var.ami_id
  instance_type = "c5.large"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]
  
  # Enable enhanced networking
  root_block_device {
    volume_type = "gp3"
    volume_size = 100
    iops        = 4000
    throughput  = 125
  }
  
  # Enable detailed monitoring
  monitoring = true
  
  # Enable enhanced networking
  credit_specification {
    cpu_credits = "unlimited"
  }
  
  tags = {
    Name = "web-${count.index + 1}"
    Environment = var.environment
  }
}

# Create a placement group for low-latency networking
resource "aws_placement_group" "web" {
  name     = "web-placement-group"
  strategy = "cluster"
}

# Rest of resources unchanged
"""
            }
        })
        
        # Mock response for architecture suggestions
        self.register_mock_response("suggest_architecture", {
            "architecture_overview": "Scalable, highly available web application architecture on AWS with multi-AZ deployment",
            "components": [
                {
                    "name": "VPC",
                    "type": "aws_vpc",
                    "description": "Isolated network environment"
                },
                {
                    "name": "Application Load Balancer",
                    "type": "aws_lb",
                    "description": "Distributes traffic to web instances"
                },
                {
                    "name": "Auto Scaling Group",
                    "type": "aws_autoscaling_group",
                    "description": "Dynamically scales EC2 instances"
                },
                {
                    "name": "RDS Multi-AZ",
                    "type": "aws_db_instance",
                    "description": "Highly available database"
                },
                {
                    "name": "ElastiCache",
                    "type": "aws_elasticache_cluster",
                    "description": "In-memory caching for performance"
                },
                {
                    "name": "S3 Bucket",
                    "type": "aws_s3_bucket",
                    "description": "Static asset storage"
                }
            ],
            "communication": "Web traffic enters through ALB, which routes to web instances in multiple AZs. Instances connect to RDS for data and ElastiCache for caching.",
            "scalability": "Auto Scaling Groups handle compute scaling. RDS can be scaled vertically. ElastiCache cluster can be scaled horizontally.",
            "security": "Security groups restrict traffic. Web tier in public subnets, database in private subnets. All data encrypted in transit and at rest.",
            "cost": "Estimated $1,000-1,500/month based on medium traffic requirements",
            "diagram": """
    +--------------------+
    |                    |
    |  Internet Gateway  |
    |                    |
    +--------+-----------+
             |
             v
    +--------+-----------+
    |                    |
    |  Application LB    |
    |                    |
    +--------+-----------+
             |
             v
+------------+------------+
|            |            |
|  Auto      |  Auto      |
|  Scaling   |  Scaling   |
|  Group     |  Group     |
|  (AZ-1)    |  (AZ-2)    |
|            |            |
+------------+------------+
      |             |
      v             v
+-----+------+ +----+-------+
|            | |            |
| ElastiCache| | ElastiCache|
| (AZ-1)     | | (AZ-2)     |
|            | |            |
+-----+------+ +----+-------+
      |             |
      v             v
+-----+------+ +----+-------+
|            | |            |
| RDS Primary| | RDS Standby|
| (AZ-1)     | | (AZ-2)     |
|            | |            |
+------------+ +------------+
""",
            "terraform_example": """
# Auto Scaling Group configuration example
resource "aws_autoscaling_group" "web" {
  name                      = "${var.environment}-web-asg"
  max_size                  = 10
  min_size                  = 2
  health_check_grace_period = 300
  health_check_type         = "ELB"
  desired_capacity          = 4
  force_delete              = true
  launch_configuration      = aws_launch_configuration.web.name
  vpc_zone_identifier       = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  target_group_arns         = [aws_lb_target_group.web.arn]
  
  tag {
    key                 = "Name"
    value               = "${var.environment}-web"
    propagate_at_launch = true
  }
}
"""
        })
        
        # Mock response for right-sizing resources
        self.register_mock_response("right_size_resources", {
            "current_resources": {
                "ec2_instances": "t3.medium (2 vCPU, 4GB RAM)",
                "ebs_volumes": "100GB standard",
                "rds_instance": "Not present"
            },
            "right_sized_resources": {
                "ec2_instances": "t3.small (2 vCPU, 2GB RAM)",
                "ebs_volumes": "50GB gp3",
                "rds_instance": "Not applicable"
            },
            "efficiency_improvement": "45%",
            "recommendations": [
                {
                    "resource": "aws_instance.web",
                    "current": "t3.medium",
                    "recommendation": "t3.small",
                    "justification": "CPU utilization < 20%, memory utilization < 30%"
                },
                {
                    "resource": "root_block_device",
                    "current": "100GB",
                    "recommendation": "50GB",
                    "justification": "Disk usage < 20GB on all instances"
                }
            ],
            "template_files": {
                "main.tf": """
provider "aws" {
  region = var.region
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  tags = {
    Name = var.vpc_name
    Environment = var.environment
  }
}

# Other VPC resources unchanged

# Right-sized instance based on utilization data
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = var.ami_id
  # Right-sized from t3.medium to t3.small based on utilization data
  instance_type = "t3.small"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]
  
  root_block_device {
    # Right-sized from 100GB to 50GB based on utilization data
    volume_size = 50
    volume_type = "gp3"
  }
  
  tags = {
    Name = "web-${count.index + 1}"
    Environment = var.environment
  }
}
"""
            }
        }) 