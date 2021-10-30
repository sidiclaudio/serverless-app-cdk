from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_iam as iam,
    core
)


class SecurityStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, vpc: ec2.Vpc, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_sg = ec2.SecurityGroup(self, 'lambdasg',
                                           security_group_name='lambda-sg',
                                           allow_all_outbound=True,
                                           vpc=vpc,
                                           description='lambda security group'
                                           )

        self.bastion_sg = ec2.SecurityGroup(self, 'bastionsg',
                                            allow_all_outbound=True,
                                            description='bastion host sg',
                                            security_group_name='bastion-sg',
                                            vpc=vpc
                                            )

        self.bastion_sg.add_ingress_rule(
            ec2.Peer.ipv4(), ec2.Port.tcp(22), 'SSH from anywhere')
