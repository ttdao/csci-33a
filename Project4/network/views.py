import random

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator

from .models import User, Post, Profile, Comment, Follow, Like


class CreatePost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(), label="post")

class EditPost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(), label="post")

# class CreateProfile(forms.Form):
#     description = forms.CharField(label=desc)
#     prof_pic = forms.CharField(label=pic)

# Show all posts on the front page and order from new to old
def index(request):

    all_posts: Post.objects.order_by("-date").all()

    paginator = Paginator(all_posts,5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)


    return render(request, "network/index.html", {
            "page_obj": page_object,
            "post_form": CreatePost(),

    })

# Get user profile by (str)username and their posts ordered by recent posts
def get_profile(request, username):
    #Get User profile if it exists
    try:
        get_profile = Profile.objects.get(username=username)
        user = get_profile.user_id
    except Profile.DoesNotExist:
        return render(request, "network/error.html",{
            "message": "Profile does not exist! Are you this is right?",
        })

    # Get all posts
    get_posts = Post.objects.filter(user=user)

    return render(request, "network/profile.html", {
        "username": username,
        "prof_posts": get_profile,
    })

# Create new post - DONE
@login_required (login_url="network:login")
def create_post(request):
    if request.method == "POST:":
        new_post = CreatePost(request.POST)

        #if form is valid
        if new_post.is_valid():
            #Find User based on the ID
            user = User.objects.get(pk=request.user.id)

            # Get clean post
            post = new_post.cleaned_data["post"]

            # Save Post
            save_post = Post.objects.create(
                user=user,
                user_post=post,
                posting_date=datetime.datetime.today(),
                posting_time=datetime.datetime.now(),
                num_likes=0,
                num_followers=0,
            )
            save_post.save()
            # Get username from profile
            # get_post = Profile.objects.get(pk=save_post.username)

            #Go back to Homepage

            return HttpResponseRedirect(reverse('network:index', args=()))

        #if invalid, stay on the page
        else:
            return render(request, "network/index.html",{
                "post_form": new_post,
            })

        # if method is GET, go to create post
    else:
        return render(request, "network/index.html", {
            "post_form": CreatePost(),
        })


# Make sure someone is logged in before editing one of their own posts
@login_required (login_url="network:login")
def edit_post(request, post_id):
    #Get post if it exists
    if request.method == "GET":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return render (request, "network/error.html", {
                "message": "Error page for Editing Post"
            })

        retrieved_post = post.user_post
        # retrieved_img = post.post_pic

        # Pre-populate form with post
        edit_form = EditPost(initial={
            "post": retrieved_post,
            # "img": retrieved_img
        })

        return render(request, "network/index.html", {
            "edit_form": edit_form,
            "post_id": post_id,
        })

    #When it is POST
    else:
        edit_form = EditPost(request.POST)

        if edit_form.is_valid():
            edited = edit_form.cleaned_data["post"]

            # Update Object




# Get followed posts - DONE
@login_required (login_url="network:login")
def follow_action(request, user_id):
    # Query to see it is following
    try:
        follow_exist = Follow.objects.get(user=request.user, followed_user=user_id)

    # If it does not exist
    except Follow.DoesNotExist:

        # See if User exists
        try:
            find_user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return render(request, "network/error.html", {
                "message": "404 User Not Found",
            })
        else:
            new_follow = Follow(
                user=request.user,
                followed_user=find_user
            )
            new_follow.save()
    # If it does exist, unfollow
    else:
        follow_exist.delete()

    username = Profile.objects.get(user=request.user).username

    #Check if follow is true
    return HttpResponseRedirect(reverse("network:get_profile", args=[username,]))




# Create Comment on Post
def comment_post(request):

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
