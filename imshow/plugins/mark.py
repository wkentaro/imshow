import argparse
import os
import sys
from typing import List

import numpy as np
import pyglet

from imshow.plugins import base


class Plugin(base.Plugin):
    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        base.Plugin.add_arguments(parser=parser)
        parser.add_argument(
            "--mark-file",
            default="mark.txt",
            help="file path to save marked items (default: %(default)r)",
        )

    mark_file: str
    marked_items: List[str]

    def __init__(self, args):
        super().__init__(args=args)
        self.mark_file = args.mark_file
        self.marked_items = self._read_mark_file(self.mark_file)

    def _read_mark_file(self, mark_file):
        if not os.path.exists(mark_file):
            return []
        with open(mark_file) as f:
            return [line.strip() for line in f]

    def get_image(self, item):
        image = super().get_image(item)
        if item in self.marked_items:
            image = np.pad(
                image,
                ((5, 5), (5, 5), (0, 0)),
                mode="constant",
            )
            image[:5] = (0, 255, 0)
            image[-5:] = (0, 255, 0)
            image[:, :5] = (0, 255, 0)
            image[:, -5:] = (0, 255, 0)
        else:
            image = np.pad(
                image,
                ((5, 5), (5, 5), (0, 0)),
                mode="constant",
                constant_values=127,
            )
        return image

    def get_keymap(self):
        return {
            (pyglet.window.key.M, 0): self._mark_item,
            (pyglet.window.key.M, pyglet.window.key.MOD_SHIFT): self._unmark_item,
        }

    def _unmark_item(self, state) -> bool:
        item = state.items[state.index]
        if item not in self.marked_items:
            print(f"not marked: {item!r} in {self.mark_file!r}", file=sys.stderr)
            return False

        self.marked_items.remove(item)
        with open(self.mark_file, "w") as f:
            for marked_item in self.marked_items:
                f.write(f"{marked_item}\n")
        return True

    def _mark_item(self, state) -> bool:
        with open(self.mark_file, "a+") as f:
            item = state.items[state.index]
            if item in self.marked_items:
                print(
                    f"already marked: {item!r} in {self.mark_file!r}", file=sys.stderr
                )
                return False
            else:
                f.write(f"{item}\n")
                self.marked_items.append(item)
                print(f"marked: {item!r} in {self.mark_file!r}", file=sys.stderr)
                return True
