import sys
import types
from typing import Any
from typing import Callable
from typing import Optional

import numpy as np
import pyglet

from imshow import _generators
from imshow import _pyglet


def imshow(
    items: Any,
    *,
    keymap: Optional[dict] = None,
    get_image_from_item: Optional[Callable] = None,
    get_title_from_item: Optional[Callable] = None,
) -> None:
    if not isinstance(items, (list, types.GeneratorType)):
        items = [items]
    if keymap is None:
        keymap = {}
    if get_image_from_item is None:

        def get_image_from_item(item):
            return item

    if get_title_from_item is None:

        def get_title_from_item(item):
            return str(item)

    items = _generators.CachedGenerator(iter(items))
    try:
        item = next(items)
    except StopIteration:
        print("No items to show.", file=sys.stderr)
        return
    image: np.ndarray = get_image_from_item(item)

    aspect_ratio: float = image.shape[1] / image.shape[0]  # width / height
    window = _pyglet.initialize_window(
        aspect_ratio=aspect_ratio, caption=get_title_from_item(item)
    )

    sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
        img=_pyglet.convert_to_imagedata(image)
    )
    _pyglet.centerize_sprite_in_window(sprite, window)

    @window.event
    def on_draw():
        pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        window.clear()
        sprite.draw()

    state = types.SimpleNamespace(items=items, index=0)

    def show_help(state):
        usage()

    def close_window(state):
        window.close()

    def print_item_and_index() -> None:
        total_size_str: str
        try:
            total_size_str = str(len(items))
        except TypeError:
            total_size_str = "n"
        print(
            f"[{state.index + 1}/{total_size_str}] {get_title_from_item(item)}",
            file=sys.stderr,
        )

    def update(item):
        window.set_caption(get_title_from_item(item))
        sprite.image = _pyglet.convert_to_imagedata(get_image_from_item(item))
        _pyglet.centerize_sprite_in_window(sprite, window)
        print_item_and_index()

    def next_image(state):
        try:
            try:
                item = state.items[state.index + 1]
            except IndexError:
                item = next(state.items)
            state.index += 1
            update(item)
        except StopIteration:
            pass

    def previous_image(state):
        try:
            if state.index > 0:
                item = state.items[state.index - 1]
            else:
                raise IndexError
            state.index -= 1
            update(item)
        except IndexError:
            pass

    def usage():
        print("Usage: ", file=sys.stderr)
        for (symbol, modifiers), action in keymap.items():
            symbol_string = pyglet.window.key.symbol_string(symbol).lower()
            modifiers_string = pyglet.window.key.modifiers_string(modifiers)
            if modifiers_string:
                key = f"{modifiers_string.lstrip('MOD_')}+{symbol_string}"
            else:
                key = symbol_string
            print(
                f"  {key}: {' '.join(action.__name__.split('_'))}",
                file=sys.stderr,
            )

    DEFAULT_KEYMAP = {
        (pyglet.window.key.H, 0): show_help,
        (pyglet.window.key.Q, 0): close_window,
        (pyglet.window.key.N, 0): next_image,
        (pyglet.window.key.P, 0): previous_image,
    }
    for key, action in DEFAULT_KEYMAP.items():
        if key not in keymap:
            keymap[key] = action

    usage()

    @window.event()
    def on_key_press(symbol, modifiers):
        if (symbol, modifiers) in keymap:
            if keymap[(symbol, modifiers)](state=state):
                update(state.items[state.index])

    print_item_and_index()

    pyglet.app.run()
