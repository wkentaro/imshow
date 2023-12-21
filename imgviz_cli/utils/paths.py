import os.path

import PIL.Image


def get_image_filepaths(files_or_dirs, recursive=False, filter_by_ext=True):
    supported_image_extensions = {
        ext
        for ext, fmt in PIL.Image.registered_extensions().items()
        if fmt in PIL.Image.OPEN
    }
    for file_or_dir in files_or_dirs:
        if os.path.isdir(file_or_dir) and not recursive:
            continue

        if os.path.isdir(file_or_dir):
            yield from get_image_filepaths(
                files_or_dirs=(
                    os.path.join(file_or_dir, basename)
                    for basename in sorted(os.listdir(file_or_dir))
                ),
                recursive=recursive,
                filter_by_ext=filter_by_ext,
            )
            continue

        if not filter_by_ext:
            yield file_or_dir

        if os.path.splitext(file_or_dir)[1].lower() in supported_image_extensions:
            yield file_or_dir
