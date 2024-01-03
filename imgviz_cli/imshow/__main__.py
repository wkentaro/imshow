#!/usr/bin/env python3

import argparse
import importlib.machinery
import os

import imgviz

import imgviz_cli


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
        version=f"%(prog)s {imgviz_cli.__version__}",
    )

    official_plugins = sorted(
        filename.split(".")[0]
        for filename in os.listdir(
            os.path.join(os.path.dirname(imgviz_cli.imshow.__file__), "plugins")
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
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="interval time [sec] between images when playing by 's' key. "
        "(default: %(default)s)",
    )
    args, _ = parser.parse_known_args()

    plugin = args.plugin

    if os.path.exists(plugin):
        plugin = importlib.machinery.SourceFileLoader("plugin", plugin).load_module()
    else:
        try:
            plugin = importlib.import_module(plugin)
        except ModuleNotFoundError:
            plugin = importlib.import_module(f"imgviz_cli.imshow.plugins.{plugin}")

    plugin.add_arguments(parser=parser)
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        return

    if not args.files_or_dirs:
        parser.error("the following arguments are required: files_or_dirs")
        return

    imgviz.io.pyglet_imshow(
        image=plugin.get_items(args=args),
        hook=lambda item: plugin.get_image(args=args, item=item),
        interval=args.interval,
    )
    imgviz.io.pyglet_run()


if __name__ == "__main__":
    main()
