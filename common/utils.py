from pathlib import Path
from typing import List
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def validate_file_size(file_obj: UploadedFile):
    max_size = settings.FILE_MAX_SIZE

    if file_obj.size > max_size:
        raise exceptions.ValidationError(
            f"File is too large. It should not exceed {bytes_to_mib(max_size)} MiB"
        )


def validate_file_type(file_obj: UploadedFile, allowed_types: List[str]):
    file_type = Path(file_obj.name).suffix

    if file_type not in allowed_types:
        allowed_types_str = ", ".join(allowed_types)
        raise exceptions.ValidationError(
            f"Not supported filetype. Allowed types are: {allowed_types_str}"
        )


def bytes_to_mib(value: int) -> float:
    # 1 bytes = 9.5367431640625E-7 mebibytes
    return value * 9.5367431640625e-7


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    return response


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
