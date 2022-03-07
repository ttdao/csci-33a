import random

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime

from .models import User, Listing, Bid, Comment


class CreateListing(forms.Form):
    listing_title = forms.CharField(label="title")
    starting_bid = forms.DecimalField(min_value=0.01, max_value=999999, label="asking_price")
    listing_description = forms.CharField(widget=forms.Textarea(), label="description")
    listing_pic = forms.CharField(label="img")  # input link here. placeholder
    # listing_pic = forms.ImageField()
    # Put in the html: <form method=POST" enctype="multipart/form-data">
    listing_category = forms.ChoiceField(required=True, choices=Listing.CATEGORY, widget=forms.Select(attrs={
        "class":"form-control"
    }))
    duration = forms.ChoiceField(required=True, choices=Listing.DURATION, widget=forms.Select(attrs={
        "class":"form-control"
    }))


class EditListing(forms.Form):
    listing_title = forms.CharField(label="title", required=False)
    listing_pic = forms.CharField(label="img", required=False)  # input link here. placeholder
    listing_category = forms.CharField(label="category", required=False)  # ideally dropdown. placeholder


class PostComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), label="Post Comment",
                              required=False)


class PlaceBid(forms.Form):
    bid = forms.DecimalField(min_value=0.01, max_value=999999)


# Homepage shows all active listings
def index(request):
    return render(request, "auctions/index.html", {
        "activelistings": Listing.objects.all()
    })


# @login_required(login_url="auctions:login")
# Get listing by ID
def get_listing(request, listing_id):
    # Get the listing, if it exists
    try:
        get_listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing does not exist! Are you this is right?",
        })

    # Check if it is on watchlist
    watchbutton = request.POST.get("active")
    user_watchlist = request.user.watchlist.all()

    if watchbutton is not None:
        if get_listing in user_watchlist:
            watchbutton = False
        else:
            watchbutton = True
    else:
        watchbutton = False

    # Get all comments
    comments = Comment.objects.filter(listing=listing_id)

    # Check if Auction is active
    auction = request.POST.get("auction")
    if auction is not None:
        if get_listing in user_watchlist:
            auction = False
        else:
            auction = True
    else:
        auction = False

    # Get the bids
    get_bid = Bid.objects.filter(listing=listing_id)
    # Get the total amount of bids
    total_bids = get_bid.count()
    if total_bids is not 0:
        # Get the highest bid
        highest_bid = get_bid.order_by('-bidding_price').first().bidding_price

        # get_bids = Bid.objects.filter(listing=listing_id).count()
        return render(request, "auctions/listing.html", {
            "listing": get_listing,
            "comments": comments,
            "bids": total_bids,
            "highestbid": highest_bid,
            "comment_form": PostComment(),
            "active": watchbutton,
            "watchlist": user_watchlist,
            "auction": auction
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": get_listing,
            "comments": comments,
            # "highestbid": highest_bid,
            "bids": total_bids,
            "comment_form": PostComment(),
            "active": watchbutton,
            "watchlist": user_watchlist
            "auction": auction
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Edit existing listing
@login_required(login_url="auctions:login")
def edit(request, listing_id):
    # Get listing if it exists
    if request.method == "GET":
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return render(request, "auctions/error.html", {
                "message": "Listing does not exist! Create a new listing",
            })

        retrieved_title = listing.item_name
        retrieved_img = listing.img
        retrieved_category = listing.category

        # Pre-populate form with some fields
        edit_form = EditListing(initial={
            "title": retrieved_title,
            "img": retrieved_img,
            "category": retrieved_category
        })

        return render(request, "auctions/edit.html", {
            "listing": listing_id,
            "edit": edit_form
        })

    # When it is POST
    else:
        edit_form = EditListing(request.POST)
        # Check if form data is valid
        # IF BLANK THEN TAKE OLD DATA OR IGNORED

        if edit_form.is_valid():
            title = edit_form.cleaned_data["listing_title"]
            pic = edit_form.cleaned_data["listing_pic"]
            category = edit_form.cleaned_data["listing_category"]

            # Update Object
            e = Listing.objects.get(pk=listing_id)
            e = Listing.objects.filter(pk=listing_id).update(
                item_name=title,
                img=pic,
                category=category,
            )
            # Redirect to edited listing
            return HttpResponseRedirect(reverse('auctions:item', args=(listing_id,)))

    # if INVALID, reload the page
    return render(request, "auctions/edit.html", {
        "listing": listing_id,
        "edit": EditListing(initial={
            "title": Listing.objects.get(id=listing_id).item_name,
            "img": Listing.objects.get(id=listing_id).img,
            "category": Listing.objects.get(id=listing_id).category,
        })})


@login_required(login_url="auctions:login")
def create(request):
    if request.method == "POST":

        new_listing = CreateListing(request.POST)

        # If form is valid
        if new_listing.is_valid():
            # Find User based on the ID
            user = User.objects.get(pk=request.user.id)

            # Get all clean fields
            title = new_listing.cleaned_data["listing_title"]
            description = new_listing.cleaned_data["listing_description"]
            bid = new_listing.cleaned_data["starting_bid"]
            pic = new_listing.cleaned_data["listing_pic"]
            category = new_listing.cleaned_data["listing_category"]

            # Save Listing
            l = Listing.objects.create(
                seller=user,
                item_name=title,
                description=description,
                asking_price=bid,
                img=pic,
                posting_date=datetime.datetime.today(),
                posting_time=datetime.datetime.now(),
                category=category
            )
            l.save()

            # Get Listing ID
            create_listing = Listing.objects.get(pk=l.id)

            return HttpResponseRedirect(reverse('auctions:item', args=(create_listing.id,)))

        # if form is invalid, stay on the page with filled fields
        else:
            return render(request, "auctions/listing.html", {
                "form": new_listing,
            })

    # if method is GET, go to create new listing
    else:
        return render(request, "auctions/createlisting.html", {
            "form": CreateListing()
        })


def rand(request):
    # Get list of listings
    get_listings = Listing.objects.all()
    total_listings = get_listings.count()
    # Pick number between 0 and total
    rng = random.randint(1, total_listings)
    # Store number
    # Redirect to random listing
    return HttpResponseRedirect(reverse('auctions:item', args=(rng,)))


@login_required(login_url="auctions:login")
def comment(request, listing_id):
    if request.method == "POST":

        comment_form = PostComment(request.POST)

        # If form is valid
        if comment_form.is_valid():
            # Find User based on the ID
            user = User.objects.get(pk=request.user.id)
            listing = Listing.objects.get(id=listing_id)

            # Get cleaned field
            content = comment_form.cleaned_data["content"]

            c = Comment.objects.create(
                user=user,
                listing=listing,
                comment_post=content,
                posting_date=datetime.datetime.today(),
                posting_time=datetime.datetime.now(),
            )
            c.save()

            return HttpResponseRedirect(reverse('auctions:item', args=(listing_id,)))


@login_required(login_url="auctions:login")
def edit_watchlist(request, listing_id):
    save_listing = Listing.objects.get(id=listing_id)
    user_watchlist = request.user.watchlist.all()
    user = request.user
    watchbutton = request.POST.get("active")
    if request.method == "POST":

    # Check to see if it is on watchlist
        if watchbutton == "False" or None:
            # Add to watchlist
            if save_listing not in user_watchlist:
                user.watchlist.add(save_listing)
                watchbutton = True
            # Remove from watchlist
        else:
            user.watchlist.remove(save_listing)
            watchbutton = False

            return render(request, "auctions/listing.html", {
                "listing": save_listing,
                "watchlist": user_watchlist,
                "active": watchbutton,
                "comment_form": PostComment()
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": save_listing,
            "watchlist": user_watchlist,
            "active": watchbutton,
            "comment_form": PostComment()
        })


@login_required(login_url="auctions:login")
def get_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchedlistings": request.user.watchlist.all()
    })


def categories(request):
    # Get all categories
    categories_list = Listing.CATEGORY

    # Get all auctions from each category

    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/categories.html", {
        "auctions": listings,
        "category":categories_list
    })



def bid(request):
    auction = request.POST.get("auction")
    if request.methond == "POST":
        form = PlaceBid(request.POST)
        if form.is_valid():
            bid_price = form.cleaned_data["placebid"]
            listing_id = request.POST.get("listing_id")

        # Check if bid is higher than highest bid
        user = request.user
        get_bid = Bid.objects.filter(listing=listing_id)
        highest_bid = get_bid.order_by('-bidding_price').first().bidding_price

        if highest_bid is None or bid_price > highest_bid:
            new_bid = Bid(
                listing=listing_id,
                user=user,
                bidding_price=bid_price
            )
            new_bid.save()

            return HttpResponseRedirect(reverse('auctions:item', args=(listing_id,)))
        else:
            return render(request, "auctions/error.html",{
                "message": "Too small. Error here for now"
            })
    else:
        return render(request, "auctions/error.html", {
            "message": "Invalid form. Error here for now"
        })
