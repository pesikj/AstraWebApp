import logging
import os

from django.db.models import Count
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView
from django_tables2 import tables, SingleTableView

from . import forms, models, tables, tasks
from .parser import ParserXML


class IndexView(TemplateView):
    template_name = "index.html"


class FileFieldFormView(FormView):
    form_class = forms.UploadFileForm
    template_name = "upload_file.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form_valid = form.is_valid()
        password = form.cleaned_data["password"]
        if form_valid and password == os.getenv("FORM_PASSWORD"):
            file = request.FILES["file_field"]
            version = models.UploadVersion(content=file)
            version.save()
            # tasks.parse_items.apply_async([version.pk])
            tasks.parse_items(version.pk)
            return redirect(self.success_url)
        else:
            logging.info(f"FileFieldFormView.inforrect password: {password} {os.getenv('FORM_PASSWORD')}")
            return render(request, self.template_name, {'form': form})


class InventoryItemListView(SingleTableView):
    table_class = tables.InventoryTable
    template_name = 'table.html'

    def get_queryset(self, *args, **kwargs):
        version = models.UploadVersion.objects.filter(inventoryitem__isnull=False).order_by('uploaded_on').last()
        return models.InventoryItem.objects.filter(version=version)


class Task1View(TemplateView):
    template_name = 'task_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_count = models.InventoryItem.objects.values('code').distinct().count()
        context["product_count"] = product_count
        return context


class InventoryItemReplaceablePartsListView(SingleTableView):
    table_class = tables.InventoryReplaceablePartsTable
    template_name = 'table.html'

    def get_queryset(self, *args, **kwargs):
        version = models.UploadVersion.objects.filter(inventoryitem__isnull=False).order_by('uploaded_on').last()
        return models.InventoryItem.objects.filter(version=version, not_matched_replaceable_parts__isnull=False)
