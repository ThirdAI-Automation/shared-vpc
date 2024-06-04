#!/usr/bin/env python3

import aws_cdk as cdk

from shared_vpc.shared_vpc_stack import SharedVpcStack


app = cdk.App()
SharedVpcStack(app, "SharedVpcStack")

app.synth()
