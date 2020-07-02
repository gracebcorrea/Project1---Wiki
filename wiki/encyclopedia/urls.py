from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("AlertsDjango", views.add, name="AlertsDjango"),
    path("EditPage", views.add, name="EditPage"),
    path("EntryPage", views.add, name="EntryPage"),
    path("NewPage", views.add, name="Newpage"),
    path("RandomPage", views.add, name="RandomPage")

]
