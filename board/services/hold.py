from typing import List, Optional
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from board.models import Hold
from common.services import model_update
from common.utils import validate_file_size, validate_file_type


def hold_create(
    *,
    name: str,
    model_file: UploadedFile,
    owner: User,
    image: Optional[UploadedFile] = None,
) -> Hold | None:
    validate_file_size(model_file)
    validate_file_type(model_file, allowed_types=[".stl"])

    if image:
        validate_file_size(image)
        validate_file_type(image, allowed_types=[".png"])

    # TODO:
    # Change after authentication implementation
    owner = User.objects.first()

    hold = Hold(
        name=name,
        model_file=model_file,
        owner=owner,
        uploaded_at=timezone.now(),
        image=image,
    )
    hold.full_clean()
    hold.save()

    return hold


def hold_update(*, hold: Hold, data) -> Hold:
    update_fields: List[str] = ["name", "model_file", "image"]

    hold, has_updated = model_update(instance=hold, fields=update_fields, data=data)

    # TODO:
    # rename model_file if name is changed
    # or figure out something different to keep clean filenames

    # TODO:
    # add verification if hold isn't assigned to any routes

    return hold
