from django.urls import path


from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("wiki/<str:entry>", views.EntryPage, name="EntryPage"),
    path("wiki/<str:TituloComTexto>", views.Search, name="EntryPage"),
    path("SearchResults", views.Search, name="SearchResults"),
    path("SearchResults", views.Search, name="Search"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("EditPage", views.EditPage, name="EditPage")



]
