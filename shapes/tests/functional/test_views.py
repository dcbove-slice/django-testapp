import json
from typing import Dict, List

import pytest
from django.urls import reverse

from shapes.models import Shape

GOOD_SHAPE_DATA: List[Dict] = [
    {"name": "Square", "face_count": 4, "is_sharp": True},
    {"name": "Triangle", "face_count": 3, "is_sharp": True},
    {"name": "Circle", "face_count": 1, "is_sharp": False},
]


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", GOOD_SHAPE_DATA)
def test_add_shape(client, test_data):
    shapes = Shape.objects.all()
    assert len(shapes) == 0

    url = reverse("shape-list")
    resp = client.post(
        url,
        json.dumps(test_data),
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["name"] == test_data["name"]

    shapes = Shape.objects.all()
    assert shapes[0].name == test_data["name"]
    assert len(shapes) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {"name": "Square", "face_count": "Some random number", "is_sharp": True},
        {"name": "Triangle", "face_count": 3, "is_sharp": "Maybe"},
        {"name": "Circle"},
    ],
)
def test_add_shape_fail(client, test_data):
    shapes = Shape.objects.all()
    assert len(shapes) == 0

    url = reverse("shape-list")
    resp = client.post(
        url,
        json.dumps(test_data),
        content_type="application/json",
    )
    assert resp.status_code == 400

    shapes = Shape.objects.all()
    assert len(shapes) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", GOOD_SHAPE_DATA)
def test_get_shape(client, add_shape, test_data):
    shape = add_shape(**test_data)
    url = reverse("shape-list")
    resp = client.get(f"{url}{shape.id}/")
    assert resp.status_code == 200
    assert resp.data["name"] == test_data.get("name")


@pytest.mark.django_db
def test_get_shape_fail(client):
    url = reverse("shape-list")
    resp = client.get(f"{url}foo/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_shapes(client, add_shape):
    for shape in GOOD_SHAPE_DATA:
        add_shape(**shape)

    url = reverse("shape-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.data[0]["name"] == GOOD_SHAPE_DATA[0]["name"]
    assert resp.data[1]["name"] == GOOD_SHAPE_DATA[1]["name"]
