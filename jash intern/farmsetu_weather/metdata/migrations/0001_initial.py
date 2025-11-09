# Generated manually for initial migration
from __future__ import annotations

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DataRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("year", models.PositiveIntegerField(db_index=True)),
                ("parameter", models.CharField(max_length=64, db_index=True)),
                ("region", models.CharField(max_length=64, db_index=True)),
                ("column_name", models.CharField(max_length=64, db_index=True)),
                ("value", models.FloatField()),
                ("source_url", models.TextField()),
                ("imported_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                "verbose_name": "Data Record",
                "verbose_name_plural": "Data Records",
                "ordering": ["parameter", "region", "year", "column_name"],
            },
        ),
        migrations.AddIndex(
            model_name="datarecord",
            index=models.Index(fields=["parameter", "region", "year"], name="idx_param_region_year"),
        ),
        migrations.AddIndex(
            model_name="datarecord",
            index=models.Index(fields=["column_name"], name="idx_column"),
        ),
        migrations.AddIndex(
            model_name="datarecord",
            index=models.Index(fields=["parameter", "region", "column_name"], name="idx_param_region_col"),
        ),
        migrations.AddConstraint(
            model_name="datarecord",
            constraint=models.UniqueConstraint(fields=("parameter", "region", "year", "column_name"), name="uniq_record_scope"),
        ),
    ]
