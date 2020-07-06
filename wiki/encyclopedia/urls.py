from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("<str:pagename>", views.Search, name="Search"),
    path("Search", views.Search, name="Search"),
    path("<str:pagename>", views.EntryPage, name="EntryPage"),
    path("Entrypage", views.EntryPage, name="EntryPage"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("EditPage", views.EditPage, name="EditPage"),
    path("AlertsDjango", views.AlertsDjango, name="AlertsDjango")

]
