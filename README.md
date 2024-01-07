<div align="center">
  <img src="https://github.com/wkentaro/imshow/blob/main/.readme/icon.png" width="200", height="200">
  <h1>imshow</h1>
  <p>
    <b>The Flexible Image Display</b>
  </p>
  <br>
</div>

*Imshow* is a Python app to display images.

*Imshow* gives you:

- **Fast and clean** display via OpenGL backend;
- **Flexibility** via command-line and code interfaces;
- **Customizability** via plugin system.

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

<img src="https://github.com/wkentaro/imshow/blob/main/.readme/tile_0.png" height="200"> <img src="https://github.com/wkentaro/imshow/blob/main/.readme/tile_1.png" height="150">

### `-p mark`

```
imshow examples/*[0-9].jpg -p mark --mark-file examples/mark.txt
```

<img src="https://github.com/wkentaro/imshow/blob/main/.readme/mark_0.png" height="150"> <img src="https://github.com/wkentaro/imshow/blob/main/.readme/mark_1.png" height="150"> <img src="https://github.com/wkentaro/imshow/blob/main/.readme/mark_2.png" height="150"> 

## Custom plugin

See [`plugins/base.py`](https://github.com/wkentaro/imshow/blob/main/imshow/plugins/base.py) for the most basic example.
For more examples, check [`plugins` folder](https://github.com/wkentaro/imshow/blob/main/imshow/plugins).

```bash
imshow examples/*.jpg --plugin custom_plugin.py --option1 7
```

```python
# custom_plugin.py

import imshow
from imshow.plugins import base

class Plugin(base.Plugin):
    @staticmethod
    def add_arguments(parser):
        base.Plugin.add_arguments(parser)

        # define additional command line options
        parser.add_argument("--option1", type=int, ...)

    option1: int

    def __init__(self, args):
        super().__init__(args, args)
        self.option1 = args.option1

    def get_items(self):
        # convert command line options into items to visualize.
        # each item represent the chunk that is visualized on a single window.
        yield from base.get_items()

    def get_image(self, item):
        # convert item into numpy array
        return base.get_image(item=item)

    def get_title(self, item):
        # convert item into str
        return base.get_title(item=item)
```

## License

MIT
