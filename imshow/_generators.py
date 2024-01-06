from typing import Any
import types


class CachedGenerator:
    def __init__(self, generator: types.GeneratorType) -> None:
        self._generator = generator
        self._yielded: list = []

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._generator)
        self._yielded.append(item)
        return item

    def __getitem__(self, index: int) -> Any:
        return self._yielded[index]
