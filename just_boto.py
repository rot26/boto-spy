import boto3

session = boto3.Session(region_name='us-east-1')
print(session)

def handle_after_call(*args, **kwargs):
    print(kwargs.get("event_name",None))
    print(kwargs.get("parsed", {}).get("ResponseMetadata", {}).get("RequestId", None))
    print(kwargs.get("parsed", {}).get("ResponseMetadata", {}).get("HTTPStatusCode", None))

def handle_provide_client_params(*args, **kwargs):
    print(kwargs.get("event_name",None))
    print(kwargs.get("params",None))

def handle_events(*args, **kwargs):
    # print(args)
    # print(kwargs)
    print(kwargs.get("event_name"))
    print("\t"+str(list(kwargs.keys())))

def list_functions():
    aws_lambda = session.client('lambda')
    functions = aws_lambda.list_functions()

def get_caller():
    client = session.client('sts')
    client.get_caller_identity()

def register():
    # session.events.register('*.*.*',handle_events, 'best-test')
    session.events.register('after-call.*.*', handle_after_call, 'after-call-spy')
    session.events.register('provide-client-params.*.*', handle_provide_client_params, 'provide-client-params-spy')

register()

# list_functions()
get_caller()
