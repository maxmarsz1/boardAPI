from pathlib import Path
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from board.models import Hold
from common.utils import validate_file_size, validate_file_type, handle_uploaded_file


def hold_create(*, name: str, model_file: UploadedFile, owner: User) -> Hold | None:
    # hold = Hold(name=name, owner=owner)
    print(name, model_file, owner)

    validate_file_size(model_file)

    validate_file_type(model_file, allowed_types=[".stl"])

    file_name = name

    # TODO:
    # Move path to settings
    file_type = Path(model_file.name).suffix
    file_path = Path(".") / f"{file_name}{file_type}"

    # handle_uploaded_file(Path(file_path), model_file)
    # TODO:
    # Change after authentication implementation
    owner = User.objects.first()

    hold = Hold(
        name=name, model_file=model_file, owner=owner, uploaded_at=timezone.now()
    )
    hold.full_clean()
    hold.save()

    return hold
