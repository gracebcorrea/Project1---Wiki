from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("AlertsDjango", views.AlertsDjango, name="AlertsDjango"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("EntryPage", views.EntryPage, name="EntryPage"),
    path("EditPage", views.EditPage, name="EditPage"),
    path("<str:NewEntry>",views.Entries, name="Entries")
]
