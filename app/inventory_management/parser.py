import logging

from lxml import etree
from . import models


class ParserXML:
    ITEM_FIELD_NAMES = ("code", "name")

    def __init__(self, version):
        self.version = version
        self.file = version.content

    def _parse_item(self, parsed_item):
        logging.debug("ParserXML._parse_item.start")
        output = {}
        for field in self.ITEM_FIELD_NAMES:
            output[field] = parsed_item.get(field)
        self._save_item(output)
        parsed_item.xpath("//part[@attribute_name='Náhradní díly']")
        replaceable_parts = {}
        if len(parsed_item):
            for item in parsed_item:
                replaceable_parts[item.get("code")] = item.get("name")
        output["replaceable_parts"] = replaceable_parts
        logging.debug("ParserXML._parse_item.end")
        return output

    def _save_item(self, item: dict):
        inventory_item = models.InventoryItem(**item)
        inventory_item.version = self.version
        inventory_item.save()

    def _save_items(self, items):
        items = list(filter(lambda x: x["replaceable_parts"], items))
        for item in items:
            main_item = models.InventoryItem.objects.get(code=item["key"])
            for inner_key, inner_value in item["replaceable_parts"].items():
                replaceable_item = models.InventoryItem.objects.get(code=inner_key)
                name = inner_value
                models.ReplaceableParts(main_item=main_item, replaceable_item=replaceable_item, name=name).save()

    def parse_file(self):
        logging.debug("ParserXML.parse_file.start")
        xml_string = self.file.read()
        tree = etree.fromstring(xml_string)
        items = tree.xpath('//items/item')
        items = list(map(self._parse_item, items))
        self._save_items(items)
        logging.debug("ParserXML.parse_file.end")
