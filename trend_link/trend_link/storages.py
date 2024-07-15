from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    file_overwrite = True


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
