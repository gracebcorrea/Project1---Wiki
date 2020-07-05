from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("<str:name>", views.EntryPage, name="EntryPage"),
    path("EditPage", views.EditPage, name="EditPage"),
    path("Search", views.Search, name="Search"),
    path("AlertsDjango", views.AlertsDjango, name="AlertsDjango")

]
