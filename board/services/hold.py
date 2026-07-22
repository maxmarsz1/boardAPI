from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from board.models import Hold
from common.utils import validate_file_size, validate_file_type


def hold_create(*, name: str, model_file: UploadedFile, owner: User) -> Hold | None:
    validate_file_size(model_file)
    validate_file_type(model_file, allowed_types=[".stl"])

    # TODO:
    # Change after authentication implementation
    owner = User.objects.first()

    hold = Hold(
        name=name, model_file=model_file, owner=owner, uploaded_at=timezone.now()
    )
    hold.full_clean()
    hold.save()

    return hold
