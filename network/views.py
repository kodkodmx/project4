from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import User, Post



def index(request):
    if not request.user.is_authenticated:
        posts = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts, 10) # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj,
        })

    else:
        user = User.objects.get(username=request.user.username)
        posts = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts, 10) # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj,
            "user": user,
            "logged_in_user": request.user.username
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
        user = User.objects.get(username=request.user.username)
        posts = Post.objects.all().order_by("-timestamp")
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))        
    else:
        return render(request, "network/new_post.html", {
            "logged_in_user": request.user.username
        })

    
def profile(request, username):
            user = User.objects.get(username=username)
            posts = user.posts.all().order_by("-timestamp")
            paginator = Paginator(posts, 10) # Show 10 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            followers = user.followers.all().values_list('username', flat=True)
            list_of_followers = list(followers)
            return render(request, "network/profile.html", {
                "posts": page_obj,
                "user": user,
                "logged_in_user": request.user.username,
                "followers": list_of_followers
            })

def follow(request, username):
    user = User.objects.get(username=username)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)

    if user in request.user.following.all():
        request.user.following.remove(user)
    else:
        request.user.following.add(user)
    return HttpResponseRedirect(reverse("profile", args=(username,)))

def following(request):
    user = User.objects.get(username=request.user.username)
    posts = Post.objects.filter(user__in=user.following.all()).order_by("-timestamp")
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page_obj,
        "user": user,
        "logged_in_user": request.user.username
    })

def followers(request, username):
    user = User.objects.get(username=username)
    followers = user.followers.all().values_list('username', flat=True)
    return render(request, "network/followers.html", {
        "followers": followers,
        "user": user,
        "logged_in_user": request.user.username
    })

def followings(request, username):
    user = User.objects.get(username=username)
    followings = user.following.all().values_list('username', flat=True)
    return render(request, "network/followings.html", {
        "followings": followings,
        "user": user,
        "logged_in_user": request.user.username
    })

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "network/post.html", {
        "post": post,
        "author": post.user.username,
        "logged_in_user": request.user.username
    })

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        content = request.POST["content"]
        post.content = content
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/edit.html", {
            "post": post,
            "logged_in_user": request.user.username,
            "author": post.user.username,
            "content": post.content
        })
