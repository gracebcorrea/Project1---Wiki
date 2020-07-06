from django.urls import path


from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("Search", views.Search, name="Search"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("EditPage", views.EditPage, name="EditPage"),
    path("EntryPage", views.EntryPage, name="EntryPage"),
    path("AlertsDjango", views.AlertsDjango, name="AlertsDjango"),
    path("wiki/<str:entry>", views.Search, name="EntryPage"),
    path("wiki/<str:entry>", views.EntryPage, name="EntryPage"),

]
