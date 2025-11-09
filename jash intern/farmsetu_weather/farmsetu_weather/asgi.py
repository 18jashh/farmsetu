"""ASGI config for farmsetu_weather project.

It exposes the ASGI callable as a module-level variable named ``application``.
This allows deployment on asynchronous-capable servers (e.g., uvicorn, daphne).
"""
from __future__ import annotations

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmsetu_weather.settings")

application = get_asgi_application()
