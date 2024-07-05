from typing import Annotated, Any

from fastapi import Depends

from app.libs.aws import get_dynamodb_resource

DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]
