<div align="center">
  <img src="https://github.com/wkentaro/imshow/raw/main/.readme/icon.png" width="200", height="200">
  <h1>imshow</h1>
  <p>
    <b>Flexible and Customizable Image Display</b>
  </p>
  <br>
</div>

*Imshow* is a Python app to display images.

*Imshow* gives you:

- **Flexiblity** - CLI & Python interface;
- **Customizability** - visualize any data via the plugin system;
- **Fast & clean** image display.

## Installation

```bash
python3 -m pip install imshow
```

## Usage

**Command-Line**

```bash
imshow examples/*.jpg
imshow examples --recursive  # --recursive (-r)
imshow examples -r --plugin tile --col 3  # --plugin (-p)
```

**Python**

```python
import glob

import imgviz
import imshow

images = (imgviz.io.imread(filepath) for filepath in glob.glob("examples/*.jpg"))
imshow.imshow(images)
```

## Builtin plugins

### `-p base` (**default**)

```
imshow examples/*.jpg
imshow examples --recursive  # auto-search image files
```

### `-p tile`

```
imshow examples/*.jpg -p tile --col 3 --row 3
imshow examples/*.jpg -p tile --col 3
```

<img src="https://github.com/wkentaro/imshow/raw/main/.readme/tile_0.png" height="200"> <img src="https://github.com/wkentaro/imshow/raw/main/.readme/tile_1.png" height="150">

### `-p mark`

```
imshow examples/*[0-9].jpg -p mark --mark-file examples/mark.txt
```

<img src="https://github.com/wkentaro/imshow/raw/main/.readme/mark_0.png" height="150"> <img src="https://github.com/wkentaro/imshow/raw/main/.readme/mark_1.png" height="150"> <img src="https://github.com/wkentaro/imshow/raw/main/.readme/mark_2.png" height="150"> 

## How to create custom plugin

You can pass a Python file that contains `class Plugin(base.Plugin)` to `--plugin, -p` to customize the behaviour of Imshow. Below example shows a countdown from 10 to 0 displayed as images.

<img src="https://github.com/wkentaro/imshow/raw/main/.readme/countdown_0.png" height=150> <img src="https://github.com/wkentaro/imshow/raw/main/.readme/countdown_1.png" height=150> <img src="https://github.com/wkentaro/imshow/raw/main/.readme/countdown_2.png" height=150>

See [`plugins/base.py`](https://github.com/wkentaro/imshow/blob/main/imshow/plugins/base.py) for the most basic example of scanning image files and displaying them.
For more examples, check [`plugins` folder](https://github.com/wkentaro/imshow/blob/main/imshow/plugins).

```bash
imshow examples/*.jpg --plugin examples/countdown_plugin.py --number 10
```

```python
import numpy as np
import imgviz
from imshow.plugins import base


class Plugin(base.Plugin):
    @staticmethod
    def add_arguments(parser):
        # define additional command line options
        parser.add_argument(
            "--number", type=int, default=10, help="number to count down from"
        )

    number: int

    def __init__(self, args):
        self.number = args.number

    def get_items(self):
        # convert command line options into items to visualize.
        # each item represent the chunk that is visualized on a single window.
        yield from range(self.number, -1, -1)

    def get_image(self, item):
        # convert item into numpy array
        image = np.full((240, 320, 3), 220, dtype=np.uint8)

        font_size = image.shape[0] // 2
        height, width = imgviz.draw.text_size(text=f"{item}", size=font_size)
        image = imgviz.draw.text(
            src=image,
            text=f"{item}",
            yx=(image.shape[0] // 2 - height // 2, image.shape[1] // 2 - width // 2),
            color=(0, 0, 0),
            size=font_size,
        )
        return image
```

## License

MIT
