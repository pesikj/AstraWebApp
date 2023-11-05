from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView
from django_tables2 import tables, SingleTableView

from . import forms, models, tables
from .parser import ParserXML


class IndexView(TemplateView):
    template_name = "index.html"


class FileFieldFormView(FormView):
    form_class = forms.UploadFileForm
    template_name = "upload_file.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file_field"]
            parser = ParserXML(file)
            parser.parse_file()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class InventoryItemListView(SingleTableView):
    model = models.InventoryItem
    table_class = tables.InventoryTable
    template_name = 'table.html'
