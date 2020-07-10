from django.urls import path


from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("wiki/<str:entry>", views.EntryPage, name="EntryPage"),
    path("Search", views.Search, name="Search"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("wiki/<str:title>", views.EditPage, name="EditPage")



]
