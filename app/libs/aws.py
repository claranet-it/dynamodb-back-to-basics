from typing import Annotated, Any

import boto3
from fastapi import Depends

from app.libs.settings import Settings, get_settings


def get_dynamodb_resource(get_settings=Annotated[Settings, Depends(get_settings)]):
    settings = get_settings()

    if settings.use_local_infra:
        return boto3.resource(
            "dynamodb",
            endpoint_url=settings.local_dynamodb_endpoint_url,
            aws_access_key_id=settings.local_aws_access_key_id,
            aws_secret_access_key=settings.local_aws_secret_access_key,
            region_name=settings.aws_region,
        )
    return boto3.resource("dynamodb")


DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]
