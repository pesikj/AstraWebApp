from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("upload/", views.FileFieldFormView.as_view(), name="upload_file"),
    path("inventory-table/", views.InventoryItemListView.as_view(), name="inventory_table"),
]
