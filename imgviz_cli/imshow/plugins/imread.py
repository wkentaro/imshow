import os

import imgviz
import PIL.Image


SUPPORTED_IMAGE_EXTENSIONS = {
    ext for ext, fmt in PIL.Image.registered_extensions().items() if fmt in PIL.Image.OPEN
}


def get_image_filenames(files_or_dirs, filter_by_ext=False):
    for file_or_dir in files_or_dirs:
        if os.path.isdir(file_or_dir):
            yield from get_image_filenames(
                files_or_dirs=(
                    os.path.join(file_or_dir, basename)
                    for basename in sorted(os.listdir(file_or_dir))
                ),
                filter_by_ext=True,
            )
        else:
            if filter_by_ext:
                if (
                    os.path.splitext(file_or_dir)[1].lower()
                    in SUPPORTED_IMAGE_EXTENSIONS
                ):
                    yield file_or_dir
            else:
                yield file_or_dir


def add_arguments(parser):
    pass


def get_image_from_args(args):
    return list(get_image_filenames(args.files_or_dirs))


def hook(args, image):
    return imgviz.io.imread(image)
