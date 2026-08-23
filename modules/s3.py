import pulumi
import pulumi_aws as aws

def create_s3_bucket(resource_name: str, bucket_name: str, enable_versioning: bool, tags: dict) -> aws.s3.BucketV2:
    """
    Creates a enterprise-standard S3 bucket with Encryption, Public Access Block, and Versioning.
    """
    # 1. Primary S3 Bucket
    bucket = aws.s3.BucketV2(
        resource_name,
        bucket=bucket_name,
        tags={**tags, "Name": bucket_name}
    )

    # 2. Block Public Access (Security Best Practice)
    aws.s3.BucketPublicAccessBlock(
        f"{resource_name}-pab",
        bucket=bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True
    )

    # 3. Server-side Encryption (AES256)
    aws.s3.BucketServerSideEncryptionConfigurationV2(
        f"{resource_name}-sse",
        bucket=bucket.id,
        rules=[
            aws.s3.BucketServerSideEncryptionConfigurationV2RuleArgs(
                apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationV2RuleApplyServerSideEncryptionByDefaultArgs(
                    sse_algorithm="AES256"
                )
            )
        ]
    )

    # 4. Versioning Configuration
    aws.s3.BucketVersioningV2(
        f"{resource_name}-versioning",
        bucket=bucket.id,
        versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
            status="Enabled" if enable_versioning else "Suspended"
        )
    )

    return bucket
