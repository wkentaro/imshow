from typing import List

import imgviz

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

    files_or_dirs: List[str]
    recursive: bool

    def __init__(self, args):
        self.files_or_dirs = args.files_or_dirs
        self.recursive = args.recursive

    def get_items(self):
        yield from _paths.get_image_filepaths(
            files_or_dirs=self.files_or_dirs, recursive=self.recursive
        )

    def get_image(self, item):
        return imgviz.io.imread(item)

    def get_keymap(self):
        return {}

    def get_title(self, item):
        return str(item)
