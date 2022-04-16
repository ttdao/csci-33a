
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # profile/<str:username>
    path("profile/<str:username>", views.get_profile, name="profile"),
    # profile/<str:username>/followingposts
    path("following_posts", views.follow_posts, name="following"),
    # editpost
    # allposts
]
