import boto3
import os

_client = None

def get_client():
    global _client
    if _client is None:
        endpoint = os.environ.get("DYNAMODB_ENDPOINT", None)
        if endpoint:
            _client = boto3.resource("dynamodb", endpoint_url=endpoint)
        else:
            _client = boto3.resource("dynamodb")
    return _client

def get_table():
    client = get_client()
    table_name = os.environ["DYNAMODB_TABLE"]
    return client.Table(table_name)