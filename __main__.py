import pulumi
from config import AppConfig
from modules import create_s3_bucket, create_ec2_instance

# 1. Load Stack Configuration
app_cfg = AppConfig()

# 2. Instantiate S3 Bucket Module
s3_bucket = create_s3_bucket(
    resource_name=f"{app_cfg.env}-app-s3",
    bucket_name=app_cfg.bucket_name,
    enable_versioning=(app_cfg.env == "prod"),
    tags=app_cfg.tags
)

# 3. Instantiate EC2 Instance Module
ec2_inst = create_ec2_instance(
    resource_name=f"{app_cfg.env}-app-ec2",
    instance_name=app_cfg.instance_name,
    subnet_id=app_cfg.subnet_id,
    security_group_id=app_cfg.security_group_id,
    instance_type=app_cfg.instance_type,
    storage_size_gb=app_cfg.storage_size_gb,
    key_name=app_cfg.key_name,
    tags=app_cfg.tags
)

# 4. Export Stack Outputs
pulumi.export("environment", app_cfg.env)
pulumi.export("s3_bucket_name", s3_bucket.id)
pulumi.export("s3_bucket_arn", s3_bucket.arn)
pulumi.export("ec2_instance_id", ec2_inst.id)
pulumi.export("ec2_private_ip", ec2_inst.private_ip)
pulumi.export("ec2_public_ip", ec2_inst.public_ip)
