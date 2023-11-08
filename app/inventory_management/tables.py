from django_tables2 import tables
from . import models


class InventoryTable(tables.Table):
    class Meta:
        model = models.InventoryItem
        template_name = "django_tables2/bootstrap4.html"
        fields = ("code", "name")
