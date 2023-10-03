import imgviz
import numpy as np

from imgviz_cli.imshow.plugins.imread import get_image_filenames


def add_arguments(parser):
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
        "--rotate",
        type=int,
        choices=[0, 90, 180, 270],
        help="Rotate images (default: %(default)s)",
        default=0,
    )


def get_image_from_args(args):
    image_pairs = []
    image_pair = []
    for image_filename in get_image_filenames(args.files_or_dirs):
        image_pair.append(image_filename)
        if len(image_pair) == args.row * args.col:
            image_pairs.append(image_pair)
            image_pair = []
    if image_pair:
        image_pairs.append(image_pair)
    return image_pairs


def hook(args, image):
    images = [
        np.rot90(imgviz.io.imread(image_filename), k=args.rotate // 90)
        for image_filename in image
    ]
    return imgviz.tile(
        imgs=images,
        shape=(args.row, args.col),
        border=(0, 0, 0),
        border_width=100,
    )
