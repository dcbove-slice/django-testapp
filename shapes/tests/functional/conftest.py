from typing import Callable

import pytest
from rest_framework.test import APIClient

from shapes.models import Shape
from user_app.models import CustomUser


@pytest.fixture(scope="function")
def add_shape() -> Callable[[str, int, bool], Shape]:
    def _add_shape(name: str, face_count: int, is_sharp: bool) -> Shape:
        shape = Shape.objects.create(name=name, face_count=face_count, is_sharp=is_sharp)
        return shape

    return _add_shape


@pytest.fixture
def client() -> "rest_framework.test.APIClient":
    user = CustomUser.objects.create_user(username="superuser", password="superuser")
    rest_api_client = APIClient()
    rest_api_client.force_authenticate(user=user)
    return rest_api_client
