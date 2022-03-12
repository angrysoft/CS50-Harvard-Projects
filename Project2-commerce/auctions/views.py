from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Category, Listing, User, Watchlist, Bid, Comment
from .forms import ListingBidForm, ListingForm


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
    actual_bid = (
        Bid.objects.filter(listing_id=list_id).order_by("-actual_price").first()
    )
    if request.method == "POST":
        form = ListingBidForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("bid_price") > actual_bid:
                new_bid = Bid()
                new_bid.bid_price = form.cleaned_data.get("bid_price")
                new_bid.save()

        return HttpResponseRedirect(reverse("listing", args=[list_id]))
    else:
        listing = get_object_or_404(Listing, pk=list_id)
        form = ListingBidForm()
        bids_count = listing.bid_set.count()
        last_bid_label = ""
        if bids_count:
            last_bid_label = f"Last bid by user {actual_bid.user} "
        form.fields[
            "bid_price"
        ].label = f"{bids_count} bid(s) so far. {last_bid_label}"

        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)

        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "user": user,
                "owner": listing.owner == user,
                "categories": listing.categories.all(),
                "bid_form": form,
                "comments": listing.comment_set.all(),
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


def comments(request: HttpRequest):
    pass


@login_required
def add_comment(request: HttpRequest, list_id: int) -> HttpResponse:
    pass
