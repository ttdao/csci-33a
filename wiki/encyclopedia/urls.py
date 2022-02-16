from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    # wiki/
    path("", views.index, name="index"),
    # /wiki/title
    path("<str:title>", views.entry, name="title"),
    # /wiki/results ???
    path("results", views.search, name="search")
]