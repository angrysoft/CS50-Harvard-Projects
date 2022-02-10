from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry_name>", views.entry, name="wiki"),
    path("add", views.new_page, name="newpage"),
    path("edit/<str:entry_name>", views.edit_page, name="edit"),
    path("random", views.random_page, name="randompage" )
]
