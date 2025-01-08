import pytest

from shapes.models import Shape


@pytest.mark.django_db
def test_shape_model():
    test_data = {"name": "Square", "face_count": 4, "is_sharp": False}
    shape = Shape(**test_data)
    shape.save()
    assert shape.name == test_data.get("name")
    assert shape.face_count == test_data.get("face_count")
    assert shape.is_sharp == test_data.get("is_sharp")
    assert shape.created_date
    assert shape.updated_date
    assert shape.name in str(shape)
