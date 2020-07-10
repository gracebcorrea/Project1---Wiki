from django.urls import path


from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("Wiki/<str:entry>", views.EntryPage, name="EntryPage"),
    path("Search", views.Search, name="Search"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("EditPage", views.EditPage, name="EditPage")



]
