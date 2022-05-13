from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator
from .models import User, Profile, Comment, Post, Tag
from skilltracker.forms import CreatePost, EditPost, CreateComment
from django.views.decorators.csrf import csrf_exempt


# Show all posts on front page and order from new to old
# Also show tags here; The other page is more dynamic
def index(request):
    return render(request, "skilltracker/index.html", {
    })


# Get all of my posts via user id ordering by descending date
def blog(request):
    return render(request, "skilltracker/blog.html", {
        "blogposts": Post.objects.all().order_by('-date')
    })


# DONE
@login_required(login_url="skilltracker:login")
def create(request):
    if request.method == "POST":
        new_post = CreatePost(request.POST)

        # if form is valid
        if new_post.is_valid():
            # Find User based on ID
            user = User.objects.get(pk=request.user.id)

            # Get all clean fields
            title = new_post.cleaned_data["title"]
            content = new_post.cleaned_data["content"]
            tags = new_post.cleaned_data["tag"]

            # Save post
            newpost_obj = Post.objects.create(
                user=user,
                title=title,
                content=content,
                date=datetime.datetime.today(),
            )
            newpost_obj.save()

            # Get multiple tags
            for tag in tags:
                selected = Tag.objects.get(pk=tag)
                newpost_obj.tag.add(selected)

            return HttpResponseRedirect(reverse('post', args=(newpost_obj.id,)))

        # If form is invalid, stay on the page with filled fields
        else:
            return render(request, "skilltracker/newpost.html", {
                "form": new_post,
            })

    # If method is GET, go to create new post
    else:
        return render(request, "skilltracker/newpost.html", {
            "form": CreatePost()
        })


# DONE with comments
def get_post(request, post_id):
    try:
        get_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, "skilltracker/error.html", {
            "message": "Post does not exist"
        })

    # Get all comments
    comments = Comment.objects.filter(post_id=post_id)
    num_of_comments = comments.count()

    return render(request, "skilltracker/blogpost.html", {
        "post": get_post,
        "comments": comments,
        "form": CreateComment(),
        "num": num_of_comments,
        "edit": EditPost(),
    })


@csrf_exempt
@login_required(login_url="skilltracker:login")
def likes(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post as JSON
    # See current like status
    if request.method == "GET":
        get_user_liked = post.likes.filter(id=request.user.id).exists()
        # return JsonResponse(post.serialize())
        return JsonResponse(
            {"liked": get_user_liked}, safe=False)

    # Update post after when clicked
    elif request.method == "PUT":
        data = json.loads(request.body)
        # If data's request user id is the same as the post's is_liked (Boolean)
        # Then remove user
        get_user_liked = data.get("user")
        user_liked = post.is_liked(get_user_liked)

        if user_liked:
            # post.likes.remove(id=request.user.id)
            post.likes.remove(get_user_liked)
        else:
            post.likes.add(get_user_liked)
        # Save JSON
        post.save()
        # return HttpResponse(status=204)

        return JsonResponse({
            "liked": user_liked,
        })

    # Post must be via GET or PUT)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required(login_url="skilltracker:login")
def edit_post(request, post_id):
    if request.method == "GET":
        try:
            get_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return render(request, "skilltracker/error.html", {
                "message": "Post does not exist"
            })

        retrieved_title = get_post.title
        retrieved_content = get_post.content
        # retrieved_category = post.tag

        # Pre-populate form
        edit_form = EditPost(initial={
            "title": retrieved_title,
            "content": retrieved_content
        })

        return render(request, "skilltracker/editpost.html", {
            "post": post_id,
            "edit": edit_form,
        })

    # When it is POST
    else:
        edit_form = EditPost(request.POST)

        # Check if form data is valid
        if edit_form.is_valid():
            title = edit_form.cleaned_data["post_title"]
            content = edit_form.cleaned_data["post_content"]
            # tag = edit_form.cleaned_data["post_tag"]

            # Update Object
            #     editpost_obj = Post.objects.get(pk=post_id)
            editpost_obj = Post.objects.filter(pk=post_id).update(
                title=title,
                content=content,
                # tag=tag
            )

            # Get post ID
            get_post_id = Post.objects.get(pk=editpost_obj.id)

            # Redirect to edited post
            return HttpResponseRedirect(reverse('post', args=(get_post_id,)))

    # If INVALID, reload the page
    return render(request, "skilltracker/editpost.html", {
        "post": post_id,
        "edit": EditPost(initial={
            "title": Post.objects.get(id=post_id).title,
            "content": Post.objects.get(id=post_id).content,
        })
    })


def tagged(request, tag_name):
    try:
        lower_str_tag = tag_name.lower()
        posts = Post.objects.filter(tag__name__icontains=tag_name)
        tag = Tag.objects.get(name__iexact=lower_str_tag)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Can't find any with this tag."}, status=404)
    except Tag.DoesNotExist:
        return JsonResponse({"error": "That tag name does not exist."}, status=404)

    return render(request, "skilltracker/taggedposts.html", {
        "taggedposts": posts.order_by('-date')
    })


@login_required(login_url="skilltracker:login")
def comment(request, post_id):
    if request.method == 'POST':
        comment_form = CreateComment(request.POST)

        # if form is valid
        if comment_form.is_valid():
            # Find user and post based on ID
            user = User.objects.get(pk=request.user.id)
            post = Post.objects.get(id=post_id)

            # Get clean form
            comment = comment_form.cleaned_data["comment"]

            # Create Comment Object
            new_comment_obj = Comment.objects.create(
                user=user,
                post=post,
                comment=comment,
                date=datetime.datetime.today()
            )
            new_comment_obj.save()

            # POSTs into the comment URL
            return HttpResponseRedirect(reverse('skilltracker:post', args=(post_id,)))

        # If form invalid, keep comment and reload
        else:
            return render(request, "skilltracker/blogpost.html", {
                "post": post_id,
                "form": comment_form,
                "edit": EditPost(),
            })

        # If request.method = GET, go to post
    else:
        return render(request, "skilltracker/blogpost.html", {
            "post": post_id,
            "edit": EditPost(),
            "form": CreateComment(),
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
            return HttpResponseRedirect(reverse("skilltracker:index"))
        else:
            return render(request, "skilltracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "skilltracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("skilltracker:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "skilltracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "skilltracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "skilltracker/register.html")
