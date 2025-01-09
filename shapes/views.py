from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Shape
from .serializers import ShapeSerializer


# pylint: disable=too-many-ancestors
class ShapeList(ModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def sharp_items(self, request):
        item_count = Shape.objects.filter(is_sharp=False).count()
        return Response({"sharp_items_count": item_count})


@login_required
def shapes_page(request):
    request.session["test_key"] = "test_value"

    shapes = Shape.objects.all()  # Query for all Shape objects
    return render(request, "shapes/shapes_page.html", {"shapes": shapes})
