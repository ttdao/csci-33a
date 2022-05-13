from django.contrib import admin
from django.db.models import Count
from .models import User, Profile, Post, Comment, Tag
from django.contrib.auth.admin import UserAdmin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "followers_count")

    def followers_count(self, obj):
        return obj.follower_count

    followers_count.short_description = 'Followers'
    followers_count.admin_order_field = "followers_count"

    # def followings_count(self, obj):
    #     return obj.follower_count
    #
    # follower_count.short_description = 'Following'
    # follower_count.admin_order_field = "following_count"

    def get_queryset_follower(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(followers_count=Count('follower'))

    # def get_queryset_following(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).annotate(followings_count=Count('following'))


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "user", "content")
    # list_display = ("id", "date", "user", "content", "like_count")

    # def like_count(self, obj):
    #     return obj.likes_count
    #
    # like_count.short_description = 'Likes'
    # like_count.admin_order_field = "like_count"
    #
    # def get_queryset_like(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).annotate(like_count=Count('likes'))


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment", "date")


# class TagAdmin(admin.ModelAdmin):
#     list_display = "name"


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
