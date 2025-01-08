from django.contrib import admin

from .models import Shape


# Register your models here.
@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "face_count",
        "is_sharp",
        "created_date",
        "updated_date",
    )
    list_display = (
        "id",
        "name",
        "face_count",
        "is_sharp",
        "created_date",
        "updated_date",
    )
    readonly_fields = (
        "id",
        "created_date",
        "updated_date",
    )
