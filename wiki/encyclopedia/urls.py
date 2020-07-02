from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.add, name="NewPage"),
    path("RandomPage", views.add, name="RandomPage"),
    path("EditPage", views.add, name="EditPage"),
    path("EntryPage", views.add, name="EntryPage"),
    path("AlertsDjango", views.add, name="AlertsDjango")
]
