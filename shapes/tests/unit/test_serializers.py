from shapes.serializers import ShapeSerializer


def test_valid_serializer():
    valid_serializer_data = {"name": "Square", "face_count": 4, "is_sharp": False}
    serializer = ShapeSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_serializer():
    invalid_serializer_data = {"name": "Square", "face_count": 4, "is_sharp": "i don't know"}
    serializer = ShapeSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"is_sharp": ["Must be a valid boolean."]}
