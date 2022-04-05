import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator, Page, InvalidPage
from django.core.exceptions import PermissionDenied

from network.forms import NewPostForm

from .models import User, Post


class Posts(View):
    def get(self, request: HttpRequest, username: str | None = None):
        posts = Post.objects.order_by("-edited")
        if username:
            posts = posts.filter(user__username__exact=username)

        page_no: int = int(request.GET.get("page", 1))
        paginator = Paginator(posts.all(), per_page=10, allow_empty_first_page=True)
        current_page: Page = paginator.get_page(page_no)
        results = {}
        results["results"] = []
        for post in current_page.object_list:
            current_post = post.serialize()
            current_post["likes"] = post.LikedPost.count()
            results["results"].append(current_post)

        results["paginator"] = {
            "page_list": list(
                current_page.paginator.get_elided_page_range(current_page.number)
            ),
            "has_previous": current_page.has_previous(),
            "has_next": current_page.has_next(),
            "page": page_no,
        }

        try:
            results["paginator"][
                "previous_page_number"
            ] = current_page.previous_page_number()
        except InvalidPage:
            pass

        try:
            results["paginator"]["next_page_number"] = current_page.next_page_number()
        except InvalidPage:
            pass

        return JsonResponse(results)

    @method_decorator(login_required)
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        post = Post()
        post.content = data.get("content")
        post.user = User.objects.get(pk=request.user.id)
        post.save()
        return HttpResponse("ok")

    @method_decorator(login_required)
    def put(self, request: HttpRequest):
        user = User.objects.get(pk=request.user.id)
        post: Post = get_object_or_404(Post, pk=1)
        if user != post.user:
            raise PermissionDenied


def index(request: HttpRequest):
    return render(
        request,
        "network/index.html",
        {
            "new_post_form": NewPostForm(),
        },
    )


def user_profile(request, username: str):
    user_profile = User.objects.get(username__exact=username)
    return render(
        request,
        "network/profile.html",
        {
            "profile": user_profile,
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
