from __future__ import annotations

from django.urls import path
from .views import DataRecordListView, DataRecordFilterView, StatsView

urlpatterns = [
    path("records/", DataRecordListView.as_view(), name="records-list"),
    path("records/filter/", DataRecordFilterView.as_view(), name="records-filter"),
    path("stats/", StatsView.as_view(), name="stats"),
]
