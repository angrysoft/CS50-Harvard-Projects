import re
from typing import Any, Dict, List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator, Page

from network.forms import NewPostForm

from .models import User, Post


class Posts(View):
    def get(self, request: HttpRequest, username: str | None = None):
        posts = Post.objects.order_by("-edited")
        if username:
            posts.filter(user__username__exact=username)

        paginator = Paginator(posts.all(), per_page=10, allow_empty_first_page=True)
        current_page: Page = paginator.get_page(page_no)
        results = {}
        results["results"] = current_page.object_list
        results["page_list"] = list(current_page.paginator.get_elided_page_range(current_page.number))
        return JsonResponse(results)

    @method_decorator(login_required)
    def post(self, request: HttpRequest):
        post = Post()
        post.content = request.POST.get("content")
        post.user = User.objects.get(pk=request.user.id)
        post.save()
        if next := request.POST.get("next"):
            return HttpResponseRedirect(next)
        return HttpResponse("ok")

    @method_decorator(login_required)
    def put(self, request: HttpRequest):
        post: Post = get_object_or_404(Post, pk=1)


def get_current_page(posts, page_no:int):
    paginator = Paginator(posts, per_page=10, allow_empty_first_page=True)
    current_page: Page = paginator.get_page(page_no)

    return current_page


def index(request: HttpRequest):
    post_form = NewPostForm()
    current_posts_page = get_current_page(
        Post.objects.order_by("-edited").all(), request.GET.get("page")
    )
    return render(
        request,
        "network/index.html",
        {
            "new_post_form": post_form,
            "posts_page": current_posts_page,
            "page_list": list(
                current_posts_page.paginator.get_elided_page_range(
                    current_posts_page.number
                )
            ),
        },
    )


def user_profile(request, username: str):
    user_profile = User.objects.get(username__exact=username)
    current_posts_page = get_current_page(
        Post.objects.order_by("-edited").filter(user__exact=user_profile).all(),
        request.GET.get("page"),
    )
    return render(
        request,
        "network/profile.html",
        {
            "profile": user_profile,
            "posts_page": current_posts_page,
            "page_list": list(
                current_posts_page.paginator.get_elided_page_range(
                    current_posts_page.number
                )
            ),
        },
    )


def login_view(request: HttpRequest):
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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
