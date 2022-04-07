
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # newpost
    # profile/<str:username>
    path("profile", views.get_profile, name="profile"),
    # profile/<str:username>/posts
    # editpost
    # allposts
]
