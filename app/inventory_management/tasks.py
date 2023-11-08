import logging

from celery import shared_task

from inventory_management.parser import ParserXML

@shared_task
def parse_items(version_pk):
    from . import models
    logging.debug("tasks.parse_items.start")
    version = models.UploadVersion.objects.get(pk=version_pk)
    parser = ParserXML(version)
    parser.parse_file()
    logging.debug("tasks.parse_items.end")
