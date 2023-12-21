import imgviz

from imgviz import utils


def add_arguments(parser):
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="recursively search files in dirs",
    )


def get_iterable_from_args(args):
    return list(utils.get_iterable_from_args(args))


def get_image_from_entry(args, entry):
    return imgviz.io.imread(entry)
