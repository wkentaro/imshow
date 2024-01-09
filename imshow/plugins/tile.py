import itertools
import os
from typing import List

import imgviz
import numpy as np

from imshow.plugins import base

try:
    from itertools import batched  # type: ignore[attr-defined]
except ImportError:

    def batched(iterable, n):  # type: ignore[no-redef]
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
        parser.add_argument(
            "--padding-color",
            nargs=3,
            help="Padding color (default: %(default)s)",
            default=[0, 0, 0],
        )
        parser.add_argument(
            "--border-width",
            type=int,
            help="Border width (default: %(default)s)",
            default=10,
        )
        parser.add_argument(
            "--border-color",
            nargs=3,
            help="border color (default: %(default)s)",
            default=[127, 127, 127],
        )

    row: int
    col: int
    padding_color: List[int]
    border_width: int
    border_color: List[int]

    def __init__(self, args):
        super().__init__(args=args)
        self.row = args.row
        self.col = args.col
        self.padding_color = args.padding_color
        self.border_width = args.border_width
        self.border_color = args.border_color

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
            cval=self.padding_color,
            border=self.border_color,
            border_width=self.border_width,
        )

    def get_title(self, item):
        root_path = os.path.dirname(item[0])
        title = [item[0]]
        for filepath in item[1:]:
            if filepath is None:
                continue
            title.append(os.path.relpath(filepath, root_path))
        return ", ".join(title)
