from __future__ import annotations

from django.apps import AppConfig


class MetdataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "metdata"
    verbose_name = "MetOffice Data"
