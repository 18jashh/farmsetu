import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmsetu_weather.settings")
django.setup()

from metdata.models import DataRecord

total = DataRecord.objects.count()
print(f"Total records: {total}")

columns = list(DataRecord.objects.values_list('column_name', flat=True).distinct())
print(f"Distinct columns: {columns}")

ann_count = DataRecord.objects.filter(column_name="ANN").count()
print(f"ANN records: {ann_count}")

sample = DataRecord.objects.filter(parameter="Tmax", region="UK")[:5]
for rec in sample:
    print(f"  {rec.year} | {rec.column_name} | {rec.value}")
