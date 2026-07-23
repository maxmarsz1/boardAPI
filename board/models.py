from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework.fields import MaxValueValidator, MinValueValidator

from common.models import BaseModel


def validate_div_five(value):
    if value % 5 != 0:
        raise ValidationError(
            _("%(value)s is not a number divisible by 5"),
            params={"value": value},
        )


def hold_upload_path(instance, filename):
    # TODO:
    # Move path to settings variable
    return "assets/holds/models/" + instance.name + ".stl"


class Hold(BaseModel):
    class Type(models.TextChoices):
        ALL = "ALL", "All"
        FEET = "FEET", "Feet"
        START = "START", "Start"
        END = "END", "End"

    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="assets/holds/images", null=True, blank=True)
    model_file = models.FileField(upload_to=hold_upload_path)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_holds",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        owner = self.owner.username if self.owner else "Unknown"
        return f"{self.name} by {owner}"

    @property
    def url(self):
        return f"{settings.APP_DOMAIN}{self.model_file.url}"


class Layout(BaseModel):
    name = models.CharField(max_length=10, unique=True)
    rows = models.PositiveSmallIntegerField()
    cols = models.PositiveSmallIntegerField()
    holds = models.ManyToManyField(Hold, through="LayoutHold")
    preview_image = models.ImageField(
        upload_to="assets/layouts/previews/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.cols}x{self.rows})"


class LayoutHold(BaseModel):
    layout = models.ForeignKey(
        Layout, related_name="layout_holds", on_delete=models.CASCADE
    )
    hold = models.ForeignKey(Hold, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()
    rotation = models.PositiveSmallIntegerField(validators=[MaxValueValidator(359)])

    class Meta:
        unique_together = ["layout", "index"]

    def __str__(self):
        return f"Layout {self.layout.name} - Hold {self.hold.name} at {self.index}({self.rotation}°)"


class Route(BaseModel):
    name = models.CharField(max_length=18)

    # TODO:
    # Make grade field implement choices
    # Predefined grades with their conversion
    grade = models.CharField(max_length=5)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_routes",
        on_delete=models.SET_NULL,
        null=True,
    )
    layout = models.ForeignKey(
        Layout, related_name="layout_routes", on_delete=models.CASCADE
    )
    tilt = models.PositiveSmallIntegerField(
        validators=[validate_div_five, MinValueValidator(0), MaxValueValidator(75)]
    )

    class Meta:
        unique_together = ["name", "layout"]

    def __str__(self):
        username = self.owner.username if self.owner else "Unknown"
        return f"{self.name}@{self.tilt}° by {username}"


class RouteHold(BaseModel):
    route = models.ForeignKey(
        Route, related_name="hold_types", on_delete=models.CASCADE
    )
    index = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=5, choices=Hold.Type.choices)

    def __str__(self):
        return f"{self.route.name} - index: {self.index} type: {self.type}"

    class Meta:
        unique_together = ["route", "index"]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                condition=models.Q(type__in=Hold.Type.values),
            )
        ]
