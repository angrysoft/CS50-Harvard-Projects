from django.contrib import admin

from .models import Category, Listing, Bid, Comment, Watchlist, User


class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories",)


admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(User)
