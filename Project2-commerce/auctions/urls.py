from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="createListing"),
    path("category/<int:category_id>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:list_id>", views.listing_details, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path(
        "watchlist-toggle/<int:list_id>",
        views.watchlist_toggle,
        name="watchlist-toggle",
    ),
    path("listing/end/<int:list_id>", views.end_auction, name="end_auction"),
    path("comments/add/<int:list_id>", views.add_comment, name="add_comment"),
]
