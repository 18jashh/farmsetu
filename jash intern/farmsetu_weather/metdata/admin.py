"""Admin configuration for metdata app."""
from __future__ import annotations

from django.contrib import admin
from .models import DataRecord


@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ("parameter", "region", "year", "column_name", "value", "imported_at")
    list_filter = ("parameter", "region", "year", "column_name")
    search_fields = ("parameter", "region", "column_name", "source_url")
    date_hierarchy = "imported_at"
    ordering = ("parameter", "region", "year", "column_name")
