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

## Builtin Plugins `--plugin` (`-p`)

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

## License

MIT
