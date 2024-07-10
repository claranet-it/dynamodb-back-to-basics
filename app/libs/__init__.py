from typing import Annotated, Any

from fastapi import Depends

from app.libs.aws import get_dynamodb_resource
from app.libs.settings import Settings, get_settings

DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]

SettingsDependency = Annotated[Settings, Depends(get_settings)]
