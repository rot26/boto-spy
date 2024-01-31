import boto3

session = boto3.Session(region_name='us-east-1')
print(session)

def handle_events(*args, **kwargs):
    # print(args)
    # print(kwargs)
    print(kwargs.get("event_name"))
    print("\t"+str(list(kwargs.keys())))


def do_calls():
    aws_lambda = session.client('lambda')
    functions = aws_lambda.list_functions()
    # aws_lambda.list_layers(CompatibleRuntime="python3.10")
    # print(functions)
    # Now make Boto3 calls using the default session.
    # client = session.client('ec2')
    # client.describe_images(DryRun=True)
    # images = client.describe_images(DryRun=False)

def register():
    event='*.*.*'
    session.events.register(event, handle_events, 'best-test')

register()

do_calls()
