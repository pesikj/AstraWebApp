from django.db import models


class UploadVersion(models.Model):
    uploaded_on = models.DateTimeField(auto_now_add=True)
    content = models.FileField()


class InventoryItem(models.Model):
    code = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    version = models.ForeignKey(UploadVersion, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_upload_version_constraint',
                fields=['code', 'version'],
            )
        ]


class ReplaceableParts(models.Model):
    main_item = models.ForeignKey("InventoryItem", on_delete=models.CASCADE, related_name="replaceable_parts")
    replaceable_item = models.ForeignKey("InventoryItem", on_delete=models.CASCADE, related_name="main_parts")
    name = models.CharField(max_length=200, null=True)

