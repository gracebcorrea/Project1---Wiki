from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("NewPage", views.add, name="NewPage"),
    path("RandomPage", views.add, name="RandomPage"),
]
