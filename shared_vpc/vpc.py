from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_iam as iam
)
from aws_cdk.aws_ec2 import CfnEIP

class VPCStack(Stack):
    def __init__(self, scope: Construct, id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        flow_log_role = iam.Role(self, f"FlowLogRole-{stage}",
            assumed_by=iam.ServicePrincipal("vpc-flow-logs.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonAPIGatewayPushToCloudWatchLogs")
            ]
        )
        
        flow_log_group = logs.LogGroup(self, f"VpcFlowLogs-{stage}",
            retention=logs.RetentionDays.ONE_MONTH  # choose retention based on your needs
        )

        if stage == "prod":
            cidr = "10.0.0.0/16"
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=20
                ),
                ec2.SubnetConfiguration(
                    name="PrivateProd",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=20
                ),
            ]
        else:
            cidr = "10.1.0.0/16"
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=20  # 4091 usable IPs
                ),
                ec2.SubnetConfiguration(
                    name="PrivateDev",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=20
                ),
                ec2.SubnetConfiguration(
                    name="PrivateShared",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=20
                ),
            ]


        self.vpc = ec2.Vpc(
            self, "VPC",
            ip_addresses=ec2.IpAddresses.cidr(cidr),
            max_azs=3,
            nat_gateways=1,  # Single NAT gateway for cost optimization
            subnet_configuration=subnet_configuration
        )

        ec2.CfnFlowLog(self, "VpcFlowLog",
            resource_id=self.vpc.vpc_id,
            resource_type="VPC",
            traffic_type="ALL",  # You can also use "REJECT" or "ACCEPT"
            deliver_logs_permission_arn=flow_log_role.role_arn,
            log_group_name=flow_log_group.log_group_name
        )

        custom_nacl = ec2.NetworkAcl(self, "CustomPrivateNACL",
            vpc=self.vpc,
            subnet_selection=ec2.SubnetSelection(subnets=self.vpc.private_subnets)
        )

        # Allow inbound from ALB to container port 8000
        custom_nacl.add_entry("AllowALBtoFargate",
            cidr=ec2.AclCidr.any_ipv4(),  # You can restrict to just the ALB IP range if known
            rule_number=100,
            traffic=ec2.AclTraffic.tcp_port(8000),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.INGRESS
        )

        # Allow inbound ephemeral return traffic
        custom_nacl.add_entry("AllowEphemeralInbound",
            cidr=ec2.AclCidr.any_ipv4(),
            rule_number=110,
            traffic=ec2.AclTraffic.tcp_port_range(1024, 65535),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.INGRESS
        )

        # Allow outbound to ALB from Fargate on port 443 or 80 (if health checks or callbacks go there)
        custom_nacl.add_entry("AllowOutboundToALB",
            cidr=ec2.AclCidr.any_ipv4(),
            rule_number=120,
            traffic=ec2.AclTraffic.tcp_port(443),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.EGRESS
        )

        # Allow outbound ephemeral for return traffic
        custom_nacl.add_entry("AllowEphemeralOutbound",
            cidr=ec2.AclCidr.any_ipv4(),
            rule_number=130,
            traffic=ec2.AclTraffic.tcp_port_range(1024, 65535),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.EGRESS
        )

        public_nacl = ec2.NetworkAcl(self, "PublicNACL",
            vpc=self.vpc,
            subnet_selection=ec2.SubnetSelection(subnets=self.vpc.public_subnets)
        )

        public_nacl.add_entry("AllowHTTPSInbound",
            rule_number=100,
            cidr=ec2.AclCidr.any_ipv4(),
            traffic=ec2.AclTraffic.tcp_port(443),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.INGRESS
        )

        public_nacl.add_entry("AllowHTTPInbound",
            rule_number=101,
            cidr=ec2.AclCidr.any_ipv4(),
            traffic=ec2.AclTraffic.tcp_port(80),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.INGRESS
        )

        public_nacl.add_entry("AllowEphemeralOutbound",
            rule_number=110,
            cidr=ec2.AclCidr.any_ipv4(),
            traffic=ec2.AclTraffic.tcp_port_range(1024, 65535),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.EGRESS
        )
        public_nacl.add_entry("AllowEphemeralInbound",
            rule_number=102,
            cidr=ec2.AclCidr.any_ipv4(),
            traffic=ec2.AclTraffic.tcp_port_range(1024, 65535),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.INGRESS
        )
        public_nacl.add_entry("AllowHTTPSOutbound",
            rule_number=103,
            cidr=ec2.AclCidr.any_ipv4(),
            traffic=ec2.AclTraffic.tcp_port(443),
            rule_action=ec2.Action.ALLOW,
            direction=ec2.TrafficDirection.EGRESS
        )

        CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        for subnet in self.vpc.public_subnets:
            name = f"{subnet.node.id}"
            CfnOutput(self, name, value=subnet.subnet_id)
            name = f"ROUTETB-{subnet.node.id}"
            CfnOutput(self, name, value=subnet.route_table.route_table_id)
            name = f"AZ-{subnet.node.id}"
            CfnOutput(self, name, value=subnet.availability_zone)
        for subnet in self.vpc.private_subnets:
            name = f"{subnet.node.id}"
            CfnOutput(self, name, value=subnet.subnet_id)
            name = f"ROUTETB-{subnet.node.id}"
            CfnOutput(self, name, value=subnet.route_table.route_table_id)
            name = f"AZ-{subnet.node.id}"
            CfnOutput(self, name, value=subnet.availability_zone)
        for resource in self.node.find_all():
            if isinstance(resource, CfnEIP):
                CfnOutput(self, "NATGatewayEIP", value=resource.ref)