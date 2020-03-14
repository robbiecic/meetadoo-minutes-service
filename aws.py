import boto3


def create_dynamodb_client():
    return boto3.client('dynamodb', region_name='ap-southeast-2', aws_access_key_id="AKIAI2BPLIHQVXLWSGCQ",
                        aws_secret_access_key="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")


def create_dynamodb_resource():
    return boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id="AKIAI2BPLIHQVXLWSGCQ",
                          aws_secret_access_key="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")
