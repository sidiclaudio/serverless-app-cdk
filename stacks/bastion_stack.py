from aws_cdk import core as cdk

from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class BastionStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bastion = ec2.Instance(self, 'bastion',
                                    instance_type=ec2.InstanceType('t2.micro'),
                                    machine_image=ec2.MachineImage.latest_amazon_linux(
                                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                        edition=ec2.AmazonLinuxEdition.STANDARD,
                                        virtualization=ec2.AmazonLinuxVirt.HVM,
                                        storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                    ),
                                    vpc=vpc,  # object instantiated in app.py
                                    # choose the subnet to place ec2 in
                                    vpc_subnets=ec2.SubnetSelection(
                                        subnet_type=ec2.SubnetType.PUBLIC
                                    ),
                                    key_name='redis-kp',
                                    security_group=sg  # passed from app.py
                                    )
