from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("areas/", views.areas_manage, name="areas_manage"),
    path("areas/create/", views.area_create, name="area_create"),
    path("areas/<int:area_id>/edit/", views.area_edit, name="area_edit"),
    path("areas/<int:area_id>/delete/", views.area_delete, name="area_delete"),

    path("items/create/", views.item_create, name="item_create"),
    path("items/<int:item_id>/toggle/", views.item_toggle, name="item_toggle"),
    path("items/<int:item_id>/delete/", views.item_delete, name="item_delete"),
]
