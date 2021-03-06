from django.contrib import admin
from .models import Post, Profile, Comment


class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "user_post", "num_likes", "posting_date", "posting_time")


class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("username", "num_followers", "prof_posts")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("username", "post_id", "prof_comment")


admin.site.register(Post, PostsAdmin)
admin.site.register(Profile, ProfilesAdmin)
admin.site.register(Comment, CommentsAdmin)
