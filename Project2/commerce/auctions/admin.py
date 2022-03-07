from django.contrib import admin
from .models import Listing, Bid, Comment


class AuctionsAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "item_name", "asking_price", "posting_date", "posting_time", "category", "img")


class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "bidding_price", "bidding_date")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "comment_post")
    # list_display = ("id", "item_name", "comment_post")


# Register your models here.
admin.site.register(Listing, AuctionsAdmin)
admin.site.register(Bid, BidsAdmin)
admin.site.register(Comment, CommentsAdmin)
