import random

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
import datetime

from .models import User, Post, Profile, Comment


class CreatePost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(), label="post")

class EditPost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(), label="post")

# class CreateProfile(forms.Form):
#     description = forms.CharField(label=desc)
#     prof_pic = forms.CharField(label=pic)

# Show all posts on the front page and order from new to old
def index(request):
    return render(request, "network/index.html", {
                  "allposts": Post.objects.all()
    })

# Get user profile by username and their posts ordered by recent posts
def get_profile(request, username):
    #Get User profile if it exists
    try:
        get_profile(Profile.objects.get(username=username))
    except Profile.DoesNotExist:
        return render(request, "network/error.html",{
            "message": "Profile does not exist! Are you this is right?",
        })

    # Get all posts
    get_posts = Post.objects.filter(username=username)

    return render(request, "network/profile.html", {
        "username": username,

    })

# Create new post
@login_required (login_url="network:login")
def create_post(request):
    if request.method == "POST:":
        new_post = CreatePost(request.POST)

        #if form is valid
        if new_post.is_valid():
            #Find User based on the ID
            user_id = User.objects.get(pk=request.user.id)

            #Get Username from the ID HERE
            user_profile = Profile.objects.get(pk=user_id)
            username = user_profile.username

            # Get clean post
            post = new_post.cleaned_data["post"]

            # Save Post
            save_post = Post.objects.create(
                #seller=user?
                username=username,
                post=post,
                like="false",
            )
            save_post.save()

            get_post = Profile.objects.get(pk=save_post.username)

            #Go back to Profile

            return HttpResponseRedirect(reverse('network:profile', args=(get_post,)))

        #if invalid, stay on the page
        else:
            return render(request, "network/profile.html")

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

        return render(request, "network/edit.html", {
            "post":

        })

    #When it is POST



# Get followers of a user
def get_followers(request):

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
