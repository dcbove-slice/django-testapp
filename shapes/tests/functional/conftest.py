from typing import Callable

import pytest

from shapes.models import Shape


@pytest.fixture(scope="function")
def add_shape() -> Callable[[str, int, bool], Shape]:
    def _add_shape(name: str, face_count: int, is_sharp: bool) -> Shape:
        shape = Shape.objects.create(name=name, face_count=face_count, is_sharp=is_sharp)
        return shape

    return _add_shape
