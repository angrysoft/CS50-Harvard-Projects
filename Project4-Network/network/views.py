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
from django.core.exceptions import ObjectDoesNotExist

from network.forms import NewPostForm

from .models import Likes, User, Post, Following


class PostView(View):
    def get(self, request: HttpRequest, post_id: int = -1):
        _post = get_object_or_404(Post, pk=post_id)
        results = {}
        results["results"] = _post.serialize()
        results["results"]["likes"] = _post.LikedPost.count()
        results["results"]["owner"] = _post.user.id == request.user.id
        return JsonResponse(results)

    @method_decorator(login_required)
    def post(self, request: HttpRequest, post_id: int | None = None):
        data = json.loads(request.body)
        post = Post()
        post.content = data.get("content")
        post.user = User.objects.get(pk=request.user.id)
        post.save()
        return HttpResponse("ok")

    @method_decorator(login_required)
    def put(self, request: HttpRequest, post_id: int):
        user = User.objects.get(pk=request.user.id)
        post: Post = get_object_or_404(Post, pk=post_id)
        if user != post.user:
            raise PermissionDenied

        data = json.loads(request.body)
        post.content = data.get("content", "")
        post.save()
        return HttpResponse("ok")


class Posts(View):
    def get(
        self,
        request: HttpRequest,
        filter_name: str | None = None,
        filter_arg: str | None = None,
    ):
        user_id: int = request.user.id
        page_no: int = int(request.GET.get("page", 1))
        posts = self.getPosts(request, filter_name, filter_arg)
        items: int = int(request.GET.get("items", 10))
        results = self.getResults(posts, user_id, page_no, items)

        return JsonResponse(results)

    def getResults(self, posts, user_id, page_no, items):
        paginator = Paginator(posts.all(), per_page=items, allow_empty_first_page=True)
        current_page: Page = paginator.get_page(page_no)
        results = {}
        results["results"] = []
        for post in current_page.object_list:
            current_post = post.serialize()
            current_post["likes"] = post.LikedPost.count()
            current_post["owner"] = post.user.id == user_id

            results["results"].append(current_post)

        results["paginator"] = {
            "page_list": list(
                current_page.paginator.get_elided_page_range(
                    current_page.number, on_each_side=1, on_ends=1
                )
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
        return results

    def getPosts(self, request, filter_name, filter_arg):
        posts = Post.objects.order_by("-edited")
        if filter_name == "username":
            posts = posts.filter(user__username__exact=filter_arg)
        elif filter_name == "following":
            if not request.user.is_authenticated:
                raise PermissionDenied

            user = User.objects.get(pk=request.user.id)
            following_users = [f.follows for f in user.Follows.all()]
            posts = posts.filter(user__username__in=following_users)
        return posts


@login_required
def likes(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        try:
            like = Likes.objects.get(user__id=request.user.id, post__id=post_id)
            like.delete()
        except ObjectDoesNotExist:
            if (post.user != request.user):
                Likes.objects.create(user=request.user, post=post)
            else:
                return HttpResponse("owner")

        return HttpResponse("ok")

    likes_count:int = post.LikedPost.count()
    return HttpResponse(likes_count)


def index(request: HttpRequest):
    return render(
        request,
        "network/index.html",
        {
            "new_post_form": NewPostForm(),
        },
    )


class UserProfile(View):
    def get(self, request: HttpRequest, username: str):
        user = User.objects.get(username__exact=username)
        user_profile = user.serialize()
        user_profile["authenticated"] = request.user.is_authenticated
        user_profile["following"] = user.Follows.count()
        user_profile["followers"] = user.Follower.count()
        user_profile["owner"] = user.id == request.user.id
        user_profile["is_followed"] = Following.objects.filter(
            follower__id=request.user.id, follows_id=user.id
        ).exists()

        return JsonResponse(user_profile)

    @method_decorator(login_required)
    def put(self, request: HttpRequest, username: str):
        user = get_object_or_404(User, pk=request.user.id)
        following_user = get_object_or_404(User, username=username)
        is_follwing = Following.objects.filter(
            follower__id=user.id, follows_id=following_user.id
        ).exists()
        if is_follwing:
            print("is_following")
            Following.objects.filter(
                follower__id=user.id, follows_id=following_user.id
            ).delete()
        else:
            print("is_not_following")
            following = Following()
            following.follower = user
            following.follows = following_user
            following.save()

        return HttpResponse("ok")


def profile(request: HttpRequest, username: str):
    return render(request, "network/profile.html", {"profile_username": username})


def following(request: HttpRequest):
    return render(request, "network/following.html")


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
