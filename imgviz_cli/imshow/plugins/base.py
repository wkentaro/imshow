import imgviz

from imgviz_cli import utils


def add_arguments(parser):
    parser.add_argument(
        "files_or_dirs",
        nargs="*",
        help="files or dirs that contain images",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="recursively search files in dirs",
    )


def get_iterable_from_args(args):
    yield from utils.get_image_filepaths(
        files_or_dirs=args.files_or_dirs, recursive=args.recursive
    )


def get_image_from_item(args, item):
    return imgviz.io.imread(item)
