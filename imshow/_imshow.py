import sys
import types
from typing import Any
from typing import Callable
from typing import Optional

import numpy as np
import pyglet

from imshow import _pyglet
from imshow import _generators


def imshow(
    items: Any,
    *,
    get_image_from_item: Optional[Callable] = None,
    get_caption_from_item: Optional[Callable] = None,
) -> None:
    if not isinstance(items, (list, types.GeneratorType)):
        items = [items]
    if get_image_from_item is None:
        get_image_from_item = lambda item: item
    if get_caption_from_item is None:
        get_caption_from_item = lambda item: str(item)

    items = _generators.CachedGenerator(iter(items))

    image: np.ndarray = (
        get_image_from_item(next(items)) if get_image_from_item else items
    )
    if not isinstance(image, np.ndarray):
        raise TypeError(
            f"get_image_from_item must return numpy.ndarray, but got {type(image)}"
        )

    aspect_ratio: float = image.shape[1] / image.shape[0]  # width / height
    window = _pyglet.initialize_window(aspect_ratio=aspect_ratio)

    sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
        _pyglet.convert_to_imagedata(image)
    )
    _pyglet.centerize_sprite_in_window(sprite, window)

    @window.event
    def on_draw():
        window.clear()
        sprite.draw()

    def usage():
        print("Usage: ", file=sys.stderr)
        print("  h: show help", file=sys.stderr)
        print("  q: close window", file=sys.stderr)
        print("  n: next image", file=sys.stderr)
        print("  p: previous image", file=sys.stderr)

    usage()

    state = types.SimpleNamespace(index=0)

    def update_with_item(item):
        window.set_caption(get_caption_from_item(item))
        sprite.image = _pyglet.convert_to_imagedata(get_image_from_item(item))
        _pyglet.centerize_sprite_in_window(sprite, window)

    @window.event()
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            window.close()
        elif symbol == pyglet.window.key.N:
            try:
                try:
                    item = items[state.index + 1]
                except IndexError:
                    item = next(items)
                update_with_item(item)
                state.index += 1
            except StopIteration:
                pass
        elif symbol == pyglet.window.key.P:
            try:
                if state.index > 0:
                    item = items[state.index - 1]
                else:
                    raise IndexError
                update_with_item(item)
                state.index -= 1
            except IndexError:
                pass
        elif symbol == pyglet.window.key.H:
            usage()
        else:
            print("Press 'h' to show help", file=sys.stderr)

    pyglet.app.run()
