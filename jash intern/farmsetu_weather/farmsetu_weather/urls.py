"""Root URL configuration for farmsetu_weather project.

The API endpoints will be added under the /api/ path when the metdata app is created.
"""
from __future__ import annotations

from django.contrib import admin
from django.urls import path, include
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index_view(request: HttpRequest) -> HttpResponse:
    """Temporary index view; will be replaced with Chart.js frontend later."""
    return render(request, "index.html", {})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_view, name="index"),
    path("api/", include("metdata.urls")),
]
