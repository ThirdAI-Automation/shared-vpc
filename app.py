#!/usr/bin/env python3

import aws_cdk as cdk
import os

from shared_vpc.shared_vpc_stack import SharedVpcStack


# Retrieve environment variables
aws_profile = os.getenv('AWS_PROFILE')
aws_account = os.getenv('CDK_DEFAULT_ACCOUNT')
aws_region = os.getenv('CDK_DEFAULT_REGION')

print(f"Using AWS profile: {aws_profile}")
print(f"Deploying to AWS account: {aws_account}")
print(f"Deploying to AWS region: {aws_region}")


app = cdk.App()
SharedVpcStack(app, "SharedVpcStack")

app.synth()
