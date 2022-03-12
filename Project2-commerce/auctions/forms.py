from pyexpat import model
from .models import Comment, Listing
from django import forms


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "categories"]
        filter_horizonal = ["categories"]


class ListingBidForm(forms.Form):
    actual_price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"required": True, "class": "form-control", "label": "Bid"}
        ),
        label="Bids",
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model: Comment