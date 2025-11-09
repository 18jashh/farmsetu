"""WSGI config for farmsetu_weather project.

It exposes the WSGI callable as a module-level variable named ``application``.
This supports traditional synchronous deployment (gunicorn/uWSGI/mod_wsgi).
"""
from __future__ import annotations

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmsetu_weather.settings")

application = get_wsgi_application()
