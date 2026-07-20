from pathlib import Path
from typing import List
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import ValidationError


def validate_file_size(file_obj: UploadedFile):
    max_size = settings.FILE_MAX_SIZE

    if file_obj.size > max_size:
        raise ValidationError(
            f"File is too large. It should not exceed {bytes_to_mib(max_size)} MiB"
        )


def validate_file_type(file_obj: UploadedFile, allowed_types: List[str]):
    file_type = Path(file_obj.name).suffix

    if file_type not in allowed_types:
        allowed_types_str = ", ".join(allowed_types)
        raise ValidationError(
            f"Not supported filetype. Allowed types are: {allowed_types_str}"
        )


def handle_uploaded_file(path: Path, file_obj: UploadedFile):
    with open(path, "wb+") as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)


def bytes_to_mib(value: int) -> float:
    # 1 bytes = 9.5367431640625E-7 mebibytes
    return value * 9.5367431640625e-7
