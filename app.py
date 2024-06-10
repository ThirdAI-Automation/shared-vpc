#!/usr/bin/env python3

import aws_cdk as cdk
import os

from shared_vpc.shared_vpc_stack import SharedVpcStack


# Retrieve environment variables
aws_profile = os.getenv('AWS_PROFILE')
aws_account = os.getenv('CDK_DEFAULT_ACCOUNT') # no need to explicitly set, if the AWS_PROFILE is properly set, this will be automatically set in the code
aws_region = os.getenv('CDK_DEFAULT_REGION') # no need to explicitly set, if the AWS_PROFILE is properly set, this will be automatically set in the code

print(f"Using AWS profile: {aws_profile}")
print(f"Deploying to AWS account: {aws_account}")
print(f"Deploying to AWS region: {aws_region}")

app = cdk.App()

ns = app.node.try_get_context("ns")

print("Namespace:", ns)


SharedVpcStack(app, f"{ns}SharedVpcStack")

app.synth()
