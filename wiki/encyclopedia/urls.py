from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:page>", views.page, name="page")
]


