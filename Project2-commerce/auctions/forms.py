
from .models import Listing
from django import forms


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "categories"]
        filter_horizonal = ["categories"]


class ListingBidForm(forms.ModelForm):
    pass