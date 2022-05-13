from django.urls import path
from . import views

app_name = "skilltracker"

urlpatterns = [
    # /skilltracker
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.create, name="create"),
    # Blog should show all posts in descending order
    path("blog", views.blog, name="blog"),
    # Get blog post
    path("blog/post/<int:post_id>", views.get_post, name="post"),
    # Edit blog post
    path("blog/edit/<int:post_id>", views.edit_post, name="edit"),
    # API Routes
    path("blog/post/likes/<int:post_id>", views.likes, name="likes"),
    # Get tagged Posts
    path("blog/taggedposts/<str:tag_name>", views.tagged, name="tagged"),
    # Leave a comment
    path("blog/post/comment/<int:post_id>", views.comment, name="comment"),
]
