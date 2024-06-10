from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)

class SharedVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "SharedVPC",
            # cidr="10.0.0.0/16",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=3,
            nat_gateways=1,  # Single NAT gateway for cost optimization
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=22  # Larger CIDR block for public subnet
                ),
                ec2.SubnetConfiguration(
                    name="PrivateProd",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,  # Use PRIVATE_WITH_EGRESS
                    cidr_mask=24  # Standard size for production
                ),
                ec2.SubnetConfiguration(
                    name="PrivateDev",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,  # Use PRIVATE_WITH_EGRESS
                    cidr_mask=24  # Standard size for development
                ),
                ec2.SubnetConfiguration(
                    name="PrivateShared",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,  # Use PRIVATE_WITH_EGRESS
                    cidr_mask=20  # Larger CIDR block for shared private subnet
                )
            ]
        )

        # # Output the VPC ID and subnet IDs for reference
        # CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        # for subnet in self.vpc.public_subnets:
        #     name = f"{id}-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.subnet_id)
        #     name = f"{id}-ROUTETB-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.route_table.route_table_id)
        #     name = f"{id}-AZ-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.availability_zone)
        # for subnet in self.vpc.private_subnets:
        #     name = f"{id}-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.subnet_id)
        #     name = f"{id}-ROUTETB-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.route_table.route_table_id)
        #     name = f"{id}-AZ-{subnet.node.id}"
        #     CfnOutput(self, name, value=subnet.availability_zone)
