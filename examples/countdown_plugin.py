import imgviz
import numpy as np

from imshow.plugins import base


class Plugin(base.Plugin):
    @staticmethod
    def add_arguments(parser):
        # define additional command line options
        parser.add_argument(
            "--number", type=int, default=10, help="number to count down from"
        )

    number: int

    def __init__(self, args):
        self.number = args.number

    def get_items(self):
        # convert command line options into items to visualize.
        # each item represent the chunk that is visualized on a single window.
        yield from range(self.number, -1, -1)

    def get_image(self, item):
        # convert item into numpy array
        image = np.full((480, 640, 3), 220, dtype=np.uint8)

        font_size = image.shape[0] // 2
        height, width = imgviz.draw.text_size(text=f"{item}", size=font_size)
        image = imgviz.draw.text(
            src=image,
            text=f"{item}",
            yx=(image.shape[0] // 2 - height // 2, image.shape[1] // 2 - width // 2),
            color=(0, 0, 0),
            size=font_size,
        )
        return image

    def get_title(self, item):
        # convert item into str
        return str(item)
