from __future__ import annotations

from rest_framework import serializers
from .models import DataRecord


class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = [
            "id",
            "year",
            "parameter",
            "region",
            "column_name",
            "value",
            "source_url",
            "imported_at",
        ]
        read_only_fields = ["id", "imported_at"]
