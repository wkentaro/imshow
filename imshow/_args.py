import glob
import os
from typing import Iterable
from typing import List


# https://github.com/pallets/click/blob/cab9483a30379f9b8e3ddb72d5a4e88f88d517b6/src/click/utils.py#L578  # noqa: E501
def expand_args(
    args: Iterable[str],
    *,
    user: bool = True,
    env: bool = True,
    glob_recursive: bool = True,
) -> List[str]:
    out = []

    for arg in args:
        if user:
            arg = os.path.expanduser(arg)

        if env:
            arg = os.path.expandvars(arg)

        matches = glob.glob(arg, recursive=glob_recursive)

        if not matches:
            out.append(arg)
        else:
            out.extend(matches)

    return out
