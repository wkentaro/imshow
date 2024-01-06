#!/usr/bin/env python3

import argparse
import importlib.machinery
import os

import imshow
from imshow.plugins import base


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--help",
        "-h",
        action="store_true",
        help="show this help message and exit",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {imshow.__version__}",
    )

    official_plugins = sorted(
        filename.split(".")[0]
        for filename in os.listdir(
            os.path.join(os.path.dirname(imshow.__file__), "plugins")
        )
        if filename.endswith(".py") and filename != "__init__.py"
    )
    parser.add_argument(
        "--plugin",
        "-p",
        default="base",
        help=f"plugin module or file path. official plugins: "
        f"{official_plugins}. (default: %(default)r)",
    )
    args, _ = parser.parse_known_args()

    plugin = args.plugin

    if os.path.exists(plugin):
        plugin = importlib.machinery.SourceFileLoader("plugin", plugin).load_module()
    else:
        try:
            plugin = importlib.import_module(plugin)
        except ModuleNotFoundError:
            plugin = importlib.import_module(f"imshow.plugins.{plugin}")

    if hasattr(plugin, "add_arguments"):
        plugin.add_arguments(parser=parser)
    else:
        base.add_arguments(parser=parser)
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        return

    if not args.files_or_dirs:
        parser.error("the following arguments are required: files_or_dirs")
        return

    if hasattr(plugin, "get_items"):
        get_items = plugin.get_items
    else:
        get_items = base.get_items

    if hasattr(plugin, "get_image"):
        get_image = plugin.get_image
    else:
        get_image = base.get_image

    imshow.imshow(
        items=get_items(args=args),
        get_image_from_item=lambda item: get_image(args=args, item=item),
    )


if __name__ == "__main__":
    main()
