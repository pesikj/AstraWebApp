from django.db import models


class UploadVersion(models.Model):
    uploaded_on = models.DateTimeField(auto_now_add=True)


class InventoryItem(models.Model):
    code = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    version = models.ForeignKey(UploadVersion, on_delete=models.CASCADE)
