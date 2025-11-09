"""Database models for the metdata app.

The core model `DataRecord` stores parsed summarised weather data from the UK MetOffice
text datasets. Each row in those datasets typically represents an annual or monthly
statistic depending on the dataset category. For this assignment we treat the first
column as the `year` (integer) and subsequent named columns map to values that may
be imported using a management command.
"""
from __future__ import annotations

from django.db import models
from django.utils import timezone


class DataRecord(models.Model):
    """A single numeric data point from a MetOffice summary dataset.

    Fields:
        year: Year associated with the observation/summary. Stored as integer for
              efficient filtering & aggregation. If a dataset includes non-numeric
              temporal labels they could be stored alternatively in a text field.
        parameter: The meteorological parameter derived from the dataset URL
                   (e.g., "Tmax", "Tmin", "Rainfall").
        region: Region code or name derived from dataset URL (e.g., "UK", "England").
        column_name: Name of the column from the source file (e.g., "JAN", "WINTER", "ANN").
        value: Floating point value for the metric.
        source_url: The full URL of the dataset from which this record originated.
        imported_at: Timestamp automatically set when the record was created.

    Indexing strategy:
        - Composite index on (parameter, region, year) improves query performance for filtering.
        - Separate index on column_name to accelerate column-based filters.
        - Additional composite index on (parameter, region, column_name) to support summary stats.

    Uniqueness:
        There can be multiple columns for the same (parameter, region, year). Enforce uniqueness
        per year/column within parameter & region scope to prevent duplicate imports.
    """

    year = models.PositiveIntegerField(db_index=True)
    parameter = models.CharField(max_length=64, db_index=True)
    region = models.CharField(max_length=64, db_index=True)
    column_name = models.CharField(max_length=64, db_index=True)
    value = models.FloatField()
    source_url = models.TextField()
    imported_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = "Data Record"
        verbose_name_plural = "Data Records"
        indexes = [
            models.Index(fields=["parameter", "region", "year"], name="idx_param_region_year"),
            models.Index(fields=["column_name"], name="idx_column"),
            models.Index(fields=["parameter", "region", "column_name"], name="idx_param_region_col"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["parameter", "region", "year", "column_name"], name="uniq_record_scope"
            )
        ]
        ordering = ["parameter", "region", "year", "column_name"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.parameter}:{self.region}:{self.year}:{self.column_name}={self.value}"