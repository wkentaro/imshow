import itertools

import imgviz
import numpy as np

from imshow.plugins import base

try:
    from itertools import batched  # type: ignore[attr-defined]
except ImportError:

    def batched(iterable, n):
        if n < 1:
            raise ValueError("n must be >= 1")
        return itertools.zip_longest(*[iter(iterable)] * n)


class Plugin(base.Plugin):
    @staticmethod
    def add_arguments(parser):
        base.Plugin.add_arguments(parser)
        parser.add_argument(
            "--row",
            type=int,
            help="Number of images in row (default: %(default)s)",
            default=1,
        )
        parser.add_argument(
            "--col",
            type=int,
            help="Number of images in column (default: %(default)s)",
            default=1,
        )

    row: int
    col: int

    def __init__(self, args):
        super().__init__(args=args)
        self.row = args.row
        self.col = args.col

    def get_items(self):
        yield from batched(super().get_items(), self.row * self.col)

    def get_image(self, item):
        images = [
            np.zeros((1, 1, 3), dtype=np.uint8)
            if filepath is None
            else imgviz.asrgb(imgviz.io.imread(filepath))
            for filepath in item
        ]
        return imgviz.tile(
            imgs=images,
            shape=(self.row, self.col),
            border=(0, 0, 0),
            border_width=100,
        )
