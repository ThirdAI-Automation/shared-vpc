
# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`shared_vpc_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

# CDK Commands
CDK Commands Can be found here 
[CDK AWS Documentation](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)

Also I initialized this project as -> [github](https://github.com/aws/aws-cdk?tab=readme-ov-file)

# How to select Profile

If you have multiple AWS Environment, just setup the one before doing `cdk deploy`
```shell
export AWS_PROFILE=YOUR_AWS_PROFILE_NAME
```

This Stack is stage agnostic, so we will simply deploy it as
```shell
cdk deploy --context ns=SAMPLE_NAME
```
Here `SAMPLE_NAME` can be anything like "infra"

Also if you have multiple AWS config, Please make use the `~/.aws/config` and `~/.aws/credentialas` files are proper and you set the appropriate profile as 
```
export AWS_PROFILE=SAMPLE_PROFILE
```

For example if you AWS Profiles are like this

```❯ cat ~/.aws/credentials
[sourav-amplify]
aws_access_key_id=AKISAMPLE
aws_secret_access_key=AKISAMPLE

[ssourav-mac]
aws_access_key_id=AKISAMPLE
aws_secret_access_key=AKISAMPLE
```

```
❯ cat ~/.aws/config
[profile sourav-amplify]
region=eu-west-1

[profile sourav-mac]
region = eu-west-1
```

And you want to use the `sourav-mac` profile then use `export AWS_PROFILE=sourav-mac`