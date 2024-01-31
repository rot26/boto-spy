import boto3
import placebo

session = boto3.Session(region_name='us-east-1')
print(session)

pill = placebo.attach(session, data_path='./.placebo')
print(pill)

# pill.record() # have to run this at least once first.
pill.playback()

print(pill)

aws_lambda = session.client('lambda')
functions = aws_lambda.list_functions()
print(functions)

# pill.playback()

# Now make Boto3 calls using the default session.
# client = session.client('ec2')
# # client.describe_images(DryRun=True)
# images = client.describe_images(DryRun=False)

print(pill)
