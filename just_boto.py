from datetime import datetime
import boto3

session = boto3.Session(region_name='us-east-1')
print(session)

def handle_after_call(*args, **kwargs):
    print(kwargs.get("event_name",None))
    print(kwargs.get("parsed", {}).get("ResponseMetadata", {}).get("RequestId", None))
    print(kwargs.get("parsed", {}).get("ResponseMetadata", {}).get("HTTPStatusCode", None))
    print(kwargs.get("parsed",{}).get("UserId",None))
    print(kwargs.get("parsed",{}).get("Account",None))

    arn = kwargs.get("parsed",{}).get("Arn",None)
    print(arn)
    arn_expanded = arn.split(":")[-1].split("/")[1:]
    print(arn_expanded)

    datestamp=kwargs.get("parsed",{}).get("ResponseMetadata",{}).get("HTTPHeaders",{}).get("date",None)
    print(datestamp)
    # convert datestamp to a datetime object
    date_object = datetime.strptime(datestamp, '%a, %d %b %Y %H:%M:%S %Z')
    print(date_object)
    # print the date object in ISO8601 format with a 'T' separator
    print(date_object.isoformat())
    # print the date object in ISO8601 format with a timzeone YYYY-MM-DDTHH:MM:SS+HH:MMZ
    print(date_object.strftime('%Y-%m-%dT%H:%M:%Sz'))
    # datestamp comes back in format 'Mon, 05 Feb 2024 22:55:54 GMT'.  We need to convert it to a unix timestamp
    print(date_object.strftime('%s'))


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
    #session.events.register('*.*.*',handle_events, 'best-test')
    session.events.register('after-call.*.*', handle_after_call, 'after-call-spy')
    session.events.register('provide-client-params.*.*', handle_provide_client_params, 'provide-client-params-spy')

register()

# list_functions()
get_caller()
