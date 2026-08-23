import pulumi
import pulumi_aws as aws

def create_ec2_instance(
    resource_name: str,
    instance_name: str,
    subnet_id: str,
    security_group_id: str,
    instance_type: str,
    storage_size_gb: int,
    key_name: str,
    tags: dict
) -> aws.ec2.Instance:
    """
    Creates an Ubuntu EC2 instance within an existing VPC Subnet & Security Group with a custom root volume size.
    """
    # 1. Dynamic Canonical Ubuntu 22.04 LTS AMI Lookup
    ubuntu_ami = aws.ec2.get_ami_output(
        most_recent=True,
        owners=["099720109477"],  # Canonical Official Owner ID
        filters=[
            aws.ec2.GetAmiFilterArgs(
                name="name",
                values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
            ),
            aws.ec2.GetAmiFilterArgs(
                name="virtualization-type",
                values=["hvm"]
            )
        ]
    )

    # 2. EC2 Instance Provisioning
    instance = aws.ec2.Instance(
        resource_name,
        ami=ubuntu_ami.id,
        instance_type=instance_type,
        subnet_id=subnet_id,
        vpc_security_group_ids=[security_group_id],
        key_name=key_name,
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            volume_size=storage_size_gb,
            volume_type="gp3",
            delete_on_termination=True,
            tags={**tags, "Name": f"{instance_name}-root-vol"}
        ),
        tags={**tags, "Name": instance_name}
    )

    return instance
