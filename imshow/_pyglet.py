from typing import Optional

import numpy as np
import PIL.Image
import pyglet


def initialize_window(
    aspect_ratio: float, caption: Optional[str] = None
) -> pyglet.window.Window:
    display: pyglet.canvas.Display = pyglet.canvas.Display()
    screen: pyglet.canvas.Screen = display.get_default_screen()

    max_window_width: int = int(round(screen.width * 0.75))
    max_window_height: int = int(round(screen.height * 0.75))

    window_width: int
    window_height: int

    # try to fit the image into the screen
    if aspect_ratio > 1:  # width > height
        window_width = max_window_width
        window_height = int(round(window_width / aspect_ratio))
    else:
        window_height = max_window_height
        window_width = int(round(window_height * aspect_ratio))

    # if still too large, shrink it
    if window_width > max_window_width:
        window_width = max_window_width
        window_height = int(round(window_width / aspect_ratio))
    if window_height > max_window_height:
        window_height = max_window_height
        window_width = int(round(window_height * aspect_ratio))

    window: pyglet.window.Window = pyglet.window.Window(
        width=window_width,
        height=window_height,
        caption=caption,
    )
    return window


def centerize_sprite_in_window(
    sprite: pyglet.sprite.Sprite, window: pyglet.window.Window
) -> None:
    scale_x = 0.95 * window.width / sprite.image.width
    scale_y = 0.95 * window.height / sprite.image.height
    scale = min(scale_x, scale_y)

    width = sprite.image.width * scale
    height = sprite.image.height * scale
    x = (window.width - width) / 2.0
    y = (window.height - height) / 2.0

    sprite.update(x=x, y=y, scale=scale)


def convert_to_imagedata(image: np.ndarray) -> pyglet.image.ImageData:
    image_pil: PIL.Image.Image = PIL.Image.fromarray(image)
    image_pil = image_pil.convert("RGB")

    kwargs = dict(
        width=image_pil.width,
        height=image_pil.height,
        data=image_pil.tobytes(),
        pitch=-image_pil.width * len(image_pil.mode),
    )
    if hasattr(pyglet, "__version__") and pyglet.__version__[0] == "2":
        kwargs["fmt"] = image_pil.mode
    else:
        kwargs["format"] = image_pil.mode
    image_pil = pyglet.image.ImageData(**kwargs)
    return image_pil
