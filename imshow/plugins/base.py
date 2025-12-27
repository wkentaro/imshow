import imgviz
import numpy as np

from imshow import _paths


class Plugin:
    @staticmethod
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
        parser.add_argument(
            "--rotate",
            type=int,
            default=0,
            choices=[0, 90, 180, 270],
            help="rotate images by 90, 180, or 270 degrees",
        )

    files_or_dirs: list[str]
    recursive: bool
    rotate: int

    def __init__(self, args):
        self.files_or_dirs = args.files_or_dirs
        self.recursive = args.recursive
        self.rotate = args.rotate

    def get_items(self):
        yield from _paths.get_image_filepaths(
            files_or_dirs=self.files_or_dirs, recursive=self.recursive
        )

    def get_image(self, item):
        image = imgviz.io.imread(item)
        if self.rotate > 0:
            image = np.rot90(image, k=self.rotate // 90)
        return image

    def get_keymap(self):
        return {}

    def get_title(self, item):
        return str(item)
