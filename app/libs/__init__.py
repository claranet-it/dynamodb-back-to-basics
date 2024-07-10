from logging import Logger
from typing import Annotated, Any

from fastapi import Depends

from app.libs.aws import get_dynamodb_resource
from app.libs.logger import get_logger
from app.libs.settings import Settings, get_settings

DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]

SettingsDependency = Annotated[Settings, Depends(get_settings)]

LoggerDependency = Annotated[Logger, Depends(get_logger)]
