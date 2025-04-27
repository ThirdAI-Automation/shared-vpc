#!/usr/bin/env python3

import aws_cdk as cdk
from shared_vpc.shared_vpc_stack import SharedVpcStack
from shared_vpc.vpc import VPCStack


app = cdk.App()
SharedVpcStack(app, "SharedVPCStack")

VPCStack(app, "VPCProd", "prod")
VPCStack(app, "VPCShared", "shared")

app.synth()
