from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("upload/", views.FileFieldFormView.as_view(), name="upload_file"),
    path("inventory-table/", views.InventoryItemListView.as_view(), name="inventory_table"),
    path("task-1/", views.Task1View.as_view(), name="task_1"),
    path("replaceable-parts/", views.InventoryItemReplaceablePartsListView.as_view(), name="replaceable_parts"),
]
