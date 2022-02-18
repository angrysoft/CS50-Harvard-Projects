from django.http import HttpRequest
from .models import Watchlist


def watchlist_no(request: HttpRequest):
    return {
        "watchlist_no": Watchlist.objects.filter(user__exact=request.user.id).count()
    }
