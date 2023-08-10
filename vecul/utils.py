import boto3
import json
import logging
import base64
from marshmallow import Schema

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

context = logging.getLogger()


class MySchema(Schema):
    error_messages = {"unknown": "Invalid Atrribute"}


db = boto3.resource("dynamodb")
table = db.Table("vecul")


def encode_to_base64(string):
    string_bytes = string.encode("utf-8")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string


def make_response(status, message, log=True):
    if log:
        context.info(f"Response: status-{status}, body-{message}")
    return {
        "statusCode": status,
        "body": json.dumps(message),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        },
    }
