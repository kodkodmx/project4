from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-timestamp").values()
    return render(request, "network/index.html", {
        "posts": posts
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
    
def new_post(request):
    if request.method == "POST":
        content = request.POST["post"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")
    
def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all().order_by("-timestamp").values()
    return render(request, "network/profile.html", {
        "posts": posts,
        "user": user
    })

def following(request):
    user = request.user
    posts = []
    for post in Post.objects.all().order_by("-timestamp").values():
        if post["user_id"] in user.following.all().values_list("id", flat=True):
            posts.append(post)
    return render(request, "network/following.html", {
        "posts": posts
    })

def followers(request, username):
    user = User.objects.get(username=username)
    followers = user.followers.all()
    return render(request, "network/followers.html", {
        "followers": followers
    })

