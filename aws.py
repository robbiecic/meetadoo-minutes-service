import boto3


def create_dynamodb_client():
    return boto3.client('dynamodb', region_name='ap-southeast-2', aws_access_key_id="AKIAJVJV2E22WXY332VA",
                        aws_secret_access_key="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")


def create_dynamodb_resource():
    return boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id="AKIAJVJV2E22WXY332VA",
                          aws_secret_access_key="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")
