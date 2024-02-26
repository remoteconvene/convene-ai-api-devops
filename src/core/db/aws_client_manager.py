import boto3

from src.core.config.settings import settings


def get_aws_client():
    try:
        return boto3.client(
            service_name=settings.AWS_SERVICE_NAME,
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY_SECRET,
        )
    except Exception as e:
        return e
