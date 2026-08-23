import pulumi

class AppConfig:
    def __init__(self):
        self.config = pulumi.Config()
        self.aws_config = pulumi.Config("aws")
        self.env = pulumi.get_stack()

        # Stack Region
        self.aws_region = self.aws_config.get("region") or "us-east-1"

        # S3 Configuration
        self.bucket_name = self.config.get("bucketName") or f"pulumi-app-s3-{self.env}"

        # Network & Security Configuration
        self.vpc_id = self.config.get("vpcId") or "vpc-0ed1afe327978a1c5"
        self.subnet_id = self.config.get("subnetId") or "subnet-06858bfcded833914"
        self.security_group_id = self.config.get("securityGroupId") or "sg-0cfa6af5ac9909993"

        # EC2 Configuration
        self.instance_name = self.config.get("instanceName") or f"pulumi-app-ec2-{self.env}"
        self.instance_type = self.config.get("instanceType") or "t3.micro"
        self.storage_size_gb = self.config.get_int("storageSizeGb") or 20
        self.key_name = self.config.get("keyName") or "packer"

        # Common Tags
        self.tags = {
            "Name": "app",
            "env": self.env,
            "ManagedBy": "Pulumi",
            "Project": "Arnav-Pulumi-Demo"
        }
