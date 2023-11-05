import pandas as pd
from django.db import transaction
from lxml import html
from . import models


class ParserXML:
    ITEM_FIELD_NAMES = ("code", "name")

    def __init__(self, file):
        self.file = file
        self.version = models.UploadVersion()
        self.version.save()

    @classmethod
    def _parse_item(cls, parsed_item):
        output = {}
        for field in cls.ITEM_FIELD_NAMES:
            output[field] = parsed_item.get(field)
        return output

    def _save_items(self, items):
        with transaction.atomic():
            for item in items:
                inventory_item = models.InventoryItem(**item)
                inventory_item.version = self.version
                inventory_item.save()

    def parse_file(self):
        xml_string = self.file.read()
        tree = html.fromstring(xml_string)
        items = tree.xpath('//item')
        items = list(map(self._parse_item, items))
        self._save_items(items)
