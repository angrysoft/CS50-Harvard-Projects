from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Category, Listing, User, Watchlist, Bid, Comment
from .forms import CommentForm, ListingBidForm, ListingForm


def index(request: HttpRequest):
    listings = Listing.objects.filter(active__exact=True).order_by("-edited")
    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
            "watchlist_no": Watchlist.objects.filter(
                user__exact=request.user.id
            ).count(),
        },
    )


def listing_details(request: HttpRequest, list_id: int):
    listing = get_object_or_404(Listing, pk=list_id)
    actual_bid = listing.bid_set.order_by("-actual_price").first()

    if request.method == "POST":
        form = ListingBidForm(request.POST)
        if form.is_valid():
            bid_price: int = form.cleaned_data.get("bid_price", 0)
            if (not actual_bid and listing.start_bid <= bid_price) or (
                actual_bid and actual_bid.actual_price < bid_price
            ):
                new_bid = Bid()
                new_bid.actual_price = bid_price
                new_bid.user = User.objects.get(pk=request.user.id)
                new_bid.listing = listing
                new_bid.save()
                return HttpResponseRedirect(reverse("listing", args=[list_id]))
            else:
                form.add_error("bid_price", "Declared Bid is to small")

    else:
        form = ListingBidForm()

    user = None
    if request.user.id:
        user = User.objects.get(pk=request.user.id)


    bids_count = listing.bid_set.count()
    last_bid_label = ""
    last_bid_user = "Unknown"
    if bids_count:
        last_bid_user = actual_bid.user
        last_bid_label = f"Last bid by user {actual_bid.user} "
    form.fields["bid_price"].label = f"{bids_count} bid(s) so far. {last_bid_label}"

    actual_price = listing.start_bid
    if bids_count:
        actual_price = actual_bid.actual_price

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "user": user,
            "owner": listing.owner == user,
            "categories": listing.categories.all(),
            "bid_form": form,
            "last_bid_user": last_bid_user,
            "actual_price": actual_price,
            "comments": listing.comment_set.all().order_by("-added"),
            "comment_form": CommentForm(),
        },
    )


@login_required
def watchlist(request: HttpRequest):
    _watchlist = Watchlist.objects.filter(user__exact=request.user.id).values_list(
        "listing", flat=True
    )
    listings = Listing.objects.filter(active__exact=True, pk__in=_watchlist).order_by(
        "-edited"
    )
    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
        },
    )


@login_required
def watchlist_toggle(request: HttpRequest, list_id: int):
    _watchlist, created = Watchlist.objects.get_or_create(
        user_id=request.user.id, listing_id=list_id
    )
    if not created:
        _watchlist.delete()
    return HttpResponseRedirect(request.GET.get("next", reverse("index")))


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
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


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
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request: HttpRequest):
    if request.method == "POST":
        listing_form = ListingForm(request.POST)
        if listing_form.is_valid():
            new_listing = listing_form.save(commit=False)
            new_listing.owner = User.objects.get(pk=request.user.id)
            new_listing.save()
            listing_form.save_m2m()
            return HttpResponseRedirect(reverse("index"))
    else:
        listing_form = ListingForm()

    return render(
        request,
        "auctions/listing_edit.html",
        {"form": listing_form, "page_header": "Create Listings"},
    )


@login_required
def end_auction(request: HttpRequest, list_id: int) -> HttpResponse:
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_id)
        if request.user.id == listing.owner.id:
            listing.active = False
            listing.save()

    return HttpResponseRedirect(reverse("listing", args=[list_id]))


def category(request: HttpRequest, category_id: int):
    _category = Category.objects.get(pk=category_id)
    listings = _category.listings.all()
    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
        },
    )


def categories(request: HttpRequest):
    return render(
        request, "auctions/categories.html", {"categories": Category.objects.all()}
    )


@login_required
def add_comment(request: HttpRequest, list_id: int) -> HttpResponse:
    if request.method == "POST":
        comment_obj = Comment()
        comment_obj.autor = User.objects.get(pk=request.user.id)
        comment_obj.listing = Listing.objects.get(pk=list_id)
        comment = CommentForm(request.POST, instance=comment_obj)
        if comment.is_valid():
            comment.save()
    return HttpResponseRedirect(reverse("listing", args=[list_id]))
