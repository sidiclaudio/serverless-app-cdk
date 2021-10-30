from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    core
)


class VpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        # Instance of vpc class
        self.vpc = ec2.Vpc(self, 'devVPC',
                           cidr="172.32.0.0/16",
                           max_azs=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="Public",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="Private",
                                   subnet_type=ec2.SubnetType.PRIVATE,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="Isolated",
                                   subnet_type=ec2.SubnetType.ISOLATED,
                                   cidr_mask=24
                               )
                           ],
                           nat_gateways=1
                           )

        # looping through all private subnets to retrive subnet ids
        priv_subnet = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1
        # storing subnet ids into parameter store
        for ps in priv_subnet:
            ssm.StringParameter(self, 'private-subnet-'+str(count),
                                string_value=ps,
                                parameter_name='/root' +
                                '/private-subnet-' + str(count)
                                )
            count += 1
