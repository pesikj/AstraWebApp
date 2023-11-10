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
        parts = parsed_item.xpath(".//part[@name='Náhradní díly']")
        replaceable_parts = {}
        for part in parts:
            for item in part:
                if item is not None:
                    replaceable_parts[item.get("code")] = item.get("name")
        output["replaceable_parts"] = replaceable_parts
        logging.debug("ParserXML._parse_item.end")
        return output

    def _save_item(self, item: dict):
        inventory_item = models.InventoryItem(**item)
        inventory_item.version = self.version
        inventory_item.save()

    def _save_items(self, items):
        items = list(filter(lambda x: len(x["replaceable_parts"]) > 0, items))
        for item in items:
            main_item_query = models.InventoryItem.objects.filter(code=item["code"], version=self.version)
            if main_item_query.count() > 0:
                main_item = main_item_query.last()
                for inner_key, inner_value in item["replaceable_parts"].items():
                    replaceable_item_query = models.InventoryItem.objects.filter(code=inner_key, version=self.version)
                    if replaceable_item_query.count() > 0:
                        replaceable_item = replaceable_item_query.last()
                        name = inner_value
                        models.ReplaceableParts(main_item=main_item,
                                                replaceable_item=replaceable_item, name=name).save()
                    if main_item.not_matched_replaceable_parts:
                        main_item.not_matched_replaceable_parts += "," + inner_key
                    else:
                        main_item.not_matched_replaceable_parts = inner_key
                    main_item.not_matched_replaceable_parts = main_item.not_matched_replaceable_parts.strip(",")
                    main_item.save()

    def parse_file(self):
        logging.debug("ParserXML.parse_file.start")
        xml_string = self.file.read()
        tree = etree.fromstring(xml_string)
        items = tree.xpath("//items/item")
        items = list(map(self._parse_item, items))
        self._save_items(items)
        logging.debug("ParserXML.parse_file.end")
