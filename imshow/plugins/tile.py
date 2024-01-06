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


def add_arguments(parser):
    base.add_arguments(parser)
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


def get_items(args):
    yield from batched(base.get_items(args), args.row * args.col)


def get_image(args, item):
    images = [
        np.zeros((1, 1, 3), dtype=np.uint8)
        if filepath is None
        else imgviz.asrgb(imgviz.io.imread(filepath))
        for filepath in item
    ]
    return imgviz.tile(
        imgs=images,
        shape=(args.row, args.col),
        border=(0, 0, 0),
        border_width=100,
    )
