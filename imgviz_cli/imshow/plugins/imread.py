import imgviz
import PIL.Image


SUPPORTED_IMAGE_EXTENSIONS = {
    ext for ext, fmt in PIL.Image.registered_extensions().items() if fmt in PIL.Image.OPEN
}


def get_image_filenames(files_or_dirs, filter_by_ext=False):
    for file_or_dir in files_or_dirs:
        if file_or_dir.isdir():
            yield from get_image_filenames(files_or_dirs=sorted(file_or_dir.listdir()), filter_by_ext=True)
        else:
            if filter_by_ext:
                if file_or_dir.ext.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                    yield file_or_dir
            else:
                yield file_or_dir


def add_arguments(parser):
    pass


def get_image_from_args(args):
    return list(get_image_filenames(args.files_or_dirs))


def hook(args, image):
    return imgviz.io.imread(image)
