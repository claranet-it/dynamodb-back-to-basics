import boto3

from app.settings import get_settings

settings = get_settings()


def get_dynamodb_resource():
    if settings.use_local_infra:
        return boto3.resource(
            "dynamodb",
            endpoint_url=settings.local_dynamodb_endpoint_url,
            aws_access_key_id=settings.local_aws_access_key_id,
            aws_secret_access_key=settings.local_aws_secret_access_key,
            region_name=settings.AWS_REGION,
        )
    return boto3.resource("dynamodb")
