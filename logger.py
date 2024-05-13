import logging
import boto3
import json
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return super(DateTimeEncoder, self).default(o)

class DynamoDBHandler(logging.Handler):
    def __init__(self, table_name):
        logging.Handler.__init__(self)
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def emit(self, record):
        try:
            self.table.put_item(Item={'id': str(record.created), 'log': self.format(record)})
        except (BotoCoreError, ClientError) as e:
            print(f"Failed to put log item to DynamoDB: {e}")

class CloudWatchHandler(logging.Handler):
    def __init__(self, log_group, stream_name):
        logging.Handler.__init__(self)
        self.logs = boto3.client('logs')
        self.log_group = log_group
        self.stream_name = stream_name

    def emit(self, record):
        try:
            response = self.logs.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.stream_name,
                logEvents=[
                    {
                        'timestamp': int(record.created * 1000),  # Convert to milliseconds
                        'message': self.format(record)
                    },
                ],
            )
        except (BotoCoreError, ClientError) as e:
            print(f"Failed to put log event to CloudWatch: {e}")

class LOGGER:
    """
    A custom logger that logs to a file, the console, DynamoDB, and CloudWatch.

    Example usage:

    ```
    logger = LOGGER('my_logger', log_file='app.log', dynamodb_table='my_table', cloudwatch_group='my_group', cloudwatch_stream='my_stream').get_logger()

    logger.info('This is an info message')
    logger.error('This is an error message')
    ```

    Parameters:
    name (str): The name of the logger.
    level (int, optional): The logging level. Defaults to logging.INFO.
    log_file (str, optional): The name of the file to log to.
    dynamodb_table (str, optional): The name of the DynamoDB table to log to. If None, DynamoDB logging is disabled. Defaults to None.
    cloudwatch_group (str, optional): The name of the CloudWatch log group to log to. If None, CloudWatch logging is disabled. Defaults to None.
    cloudwatch_stream (str, optional): The name of the CloudWatch log stream to log to. If None, CloudWatch logging is disabled. Defaults to None.
    quiet (bool, optional): If True, the logger will not log to the console. Defaults to False.
    """
    def __init__(self, name, log_level=logging.INFO, log_file_name=None, dynamodb_table=None, cloudwatch_group=None, cloudwatch_stream=None, quiet=False):
        # ...        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create a stream handler for command line output
        if not quiet:
            stream_handler = logging.StreamHandler()
            self.logger.addHandler(stream_handler)

        # Create a file handler if a log file is specified
        if log_file_name:
            file_handler = logging.FileHandler(log_file_name)
            self.logger.addHandler(file_handler)

        # Create a DynamoDB handler
        if dynamodb_table:
            dynamodb_handler = DynamoDBHandler(dynamodb_table)
            self.logger.addHandler(dynamodb_handler)

        # Create a CloudWatch handler
        if cloudwatch_group and cloudwatch_stream:
            cloudwatch_handler = CloudWatchHandler(cloudwatch_group, cloudwatch_stream)
            self.logger.addHandler(cloudwatch_handler)

    def get_logger(self):
        return self.logger
