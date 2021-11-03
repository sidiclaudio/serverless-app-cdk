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

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
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
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'SSH from anywhere')

        # Create a Lambda Role and attach a Managed policy
        self.lambda_role = iam.Role(self, 'lambdarole',
                                    assumed_by=iam.ServicePrincipal(
                                        service='lambda.amazonaws.com'),
                                    description='bastion IAM role',
                                    role_name='cdk-lambda-role',
                                    managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                        managed_policy_name='service-role/AWSLambdaVPCAccessExecutionRole'
                                    )]
                                    )
        # Attach inline policy
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            resources=['*'],
            actions=['rds:*', 's3:*']
        ))

        # SSM Parameters definition
        ssm.StringParameter(self, 'lambdasg-param',
                            parameter_name='/root' + '/lambdasg-param',
                            string_value=self.lambda_sg.security_group_id
                            )

        ssm.StringParameter(self, 'lambdarole-param-name',
                            parameter_name='/root' + '/lambdarole-param-name',
                            string_value=self.lambda_role.role_name
                            )

        ssm.StringParameter(self, 'lambdarole-param-arn',
                            parameter_name='/root' + '/lambdarole-param-arn',
                            string_value=self.lambda_role.role_arn
                            )
