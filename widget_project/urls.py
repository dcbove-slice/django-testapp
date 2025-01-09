"""
URL configuration for widget_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shapes.views import ShapeList, shapes_page

project_router = DefaultRouter()
project_router.register("shape", ShapeList, basename="shape")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(project_router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("shapes/", shapes_page, name="shapes_page"),
]
