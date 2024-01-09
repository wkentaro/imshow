import argparse
import importlib.machinery
import os
import sys

import imshow
import imshow.plugins


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
        version=f"imshow {imshow.__version__}",
    )

    official_plugins = [
        plugin for plugin in dir(imshow.plugins) if not plugin.startswith("_")
    ]
    parser.add_argument(
        "--plugin",
        "-p",
        default="base",
        help=f"plugin module or file path. official plugins: "
        f"{official_plugins}. (default: %(default)r)",
    )
    args, _ = parser.parse_known_args()

    if os.path.exists(args.plugin):
        plugin_module = importlib.machinery.SourceFileLoader(
            "plugin", args.plugin
        ).load_module()
    else:
        try:
            plugin_module = importlib.import_module(f"imshow.plugins.{args.plugin}")
        except ModuleNotFoundError:
            try:
                plugin_module = importlib.import_module(args.plugin)
            except ModuleNotFoundError:
                print(f"Error: plugin {args.plugin!r} is not found.", file=sys.stderr)
                sys.exit(1)

    plugin_module.Plugin.add_arguments(parser=parser)
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        return

    plugin = plugin_module.Plugin(args=args)

    imshow.imshow(
        items=plugin.get_items(),
        keymap=plugin.get_keymap(),
        get_image_from_item=plugin.get_image,
        get_title_from_item=plugin.get_title,
    )


if __name__ == "__main__":
    main()
