from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("AlertsDjango", views.AlertsDjango, name="AlertsDjango"),
    path("EditPage", views.EditPage, name="EditPage"),
    path("EntryPage", views.EntryPage, name="EntryPage"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("<str:entry>",views.Entries, name="entries")
]
