from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    # wiki/
    path("", views.index, name="index"),
    # /wiki/title
    path("<str:title>", views.entry, name="title"),
    # wiki/search
    path("search/", views.search, name="search"),
    # wiki/new
    path("new/", views.new, name="new"),
    # wiki/
    path("random/", views.rand, name="rand"),
    # wiki/edit
    path("edit/<str:title>", views.edit, name="edit"),
]