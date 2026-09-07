from typing import Tuple
from PIL import Image, ImageFile

from django.db.models import QuerySet

from board.models import LayoutHold


class LayoutPreviewGenerator:
    MIN_LAYOUT_WIDTH = 300
    MIN_HOLD_WIDTH = 128

    def __init__(
        self, cols: int, rows: int, layout_holds: QuerySet[LayoutHold]
    ) -> None:
        self.cols = cols
        self.rows = rows
        self.layout_holds = layout_holds
        self.hold_width = self._get_hold_width()
        self.preview_size = self._get_preview_size()

    def _get_hold_width(self) -> int:
        if self.MIN_HOLD_WIDTH * self.cols < self.MIN_LAYOUT_WIDTH:
            # we don't care if preview width isnt exactly MIN_LAYOUT_WIDTH
            # it needs to be close enough
            return self.MIN_LAYOUT_WIDTH // self.cols
        return self.MIN_HOLD_WIDTH

    def _get_preview_size(self) -> Tuple[int, int]:
        return (self.cols * self.hold_width, self.rows * self.hold_width)

    def _resize_image(self, image: ImageFile.ImageFile) -> Image.Image:
        orig_width, orig_height = image.size
        new_height = int(orig_height * (self.hold_width / orig_width))
        return image.resize((self.hold_width, new_height), Image.BICUBIC)

    def _index_to_cords(self, index: int) -> Tuple[int, int]:
        x = index % self.cols * self.hold_width
        y = index // self.cols * self.hold_width
        return (x, y)

    def generate(self) -> Image.Image:
        preview_image = Image.new("RGB", self.preview_size, "black")

        for hold in self.layout_holds:
            try:
                x, y = self._index_to_cords(hold.index)
                hold_image = Image.open(hold.hold.image)
                resized_image = self._resize_image(hold_image)
                rotated_image = resized_image.rotate(hold.rotation)
                preview_image.paste(rotated_image, (x, y))
            except ValueError:
                print("skipping, no hold image set")

        return preview_image
