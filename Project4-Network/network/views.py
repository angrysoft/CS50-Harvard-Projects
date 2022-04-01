from typing import Any, Dict, List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator, Page

from network.forms import NewPostForm

from .models import User, Post


class GenericListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        params: Dict[str, Any] = self._get_parameters(request)

        items_list: list[Dict[Any, Any]] = self._get_items(params)
        paginator = Paginator(
            items_list, per_page=params.get("items", 10), allow_empty_first_page=True
        )
        current_page: Page = paginator.get_page(params.get("page_no"))

        result: Dict[str, Any] = {
            "results": self._get_current_page(current_page),
            "pages": paginator.num_pages,
            "currentPage": current_page.number,
            "pageRange": list(paginator.get_elided_page_range(current_page.number)),
        }

        return JsonResponse(result, safe=False)

    def _get_items(self, params: Dict[str, Any]) -> list[Dict[Any, Any]]:

        return []

    def _get_parameters(self, request: HttpRequest) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        try:
            results["page_no"] = int(request.GET.get("page", "1"))
        except ValueError:
            results["page_no"] = 1
        try:
            results["items"] = int(request.GET.get("items", 10))
        except ValueError:
            results["items"] = 10

        return results

    def _get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        return []


def get_current_page(posts, page_no):
    paginator = Paginator(posts, per_page=10, allow_empty_first_page=True)
    current_page: Page = paginator.get_page(page_no)

    return current_page


def index(request):
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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
