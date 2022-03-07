from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    # auctions/
    path("", views.index, name="index"),
    # auctions/login
    path("login", views.login_view, name="login"),
    # auctions/logout
    path("logout", views.logout_view, name="logout"),
    # auctions/register
    path("register", views.register, name="register"),
    # auctions/createlisting
    path("createlisting", views.create, name="create"),
    # auctions/listing/#
    path("listing/<int:listing_id>", views.get_listing, name="item"),
    # auctions/error
    # path("error", views.error, name="error"),
    # auctions/edit/listing
    path("edit/listing/<int:listing_id>", views.edit, name="edit"),
    # auctions/rand
    path("random/", views.rand, name="rand"),
    # auctions/listing/<int:listing_id>/comment
    path("listing/<int:listing_id>/comment/", views.comment, name="comment"),
    # auctions/watchlist
    path("watchlist/", views.get_watchlist, name="watchlist"),
    # auctions/listing/<int:listing_id>/watchlist/
    path("listing/<int:listing_id>/watchlist/", views.edit_watchlist, name="edit_watchlist"),
    # auctions/categories
    # path("categories/", views.categories, name="categories"),
    # auctions/categories
    path("bid/", views.bid, name="bid"),


]