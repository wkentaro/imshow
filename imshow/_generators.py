import types
from typing import Any


class CachedGenerator:
    def __init__(self, generator: types.GeneratorType) -> None:
        self._exhausted: bool = False
        self._generator = generator
        self._yielded: list = []

    @property
    def exhausted(self) -> bool:
        return self._exhausted

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = next(self._generator)
        except StopIteration:
            self._exhausted = True
            raise StopIteration
        self._yielded.append(item)
        return item

    def __getitem__(self, index: int) -> Any:
        return self._yielded[index]

    def __len__(self) -> int:
        if self._exhausted:
            return len(self._yielded)
        else:
            raise TypeError("len() of a not fully exhausted generator is not allowed")
