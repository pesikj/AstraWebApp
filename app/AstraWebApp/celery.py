# django_celery/celery.py


import os

from celery import Celery


if os.getenv("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AstraWebApp.settings")

app = Celery("AstraWebApp")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
