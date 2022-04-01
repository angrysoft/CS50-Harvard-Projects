from cProfile import label
from attr import fields
from django import forms


class PostFrom(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={"required": True, "class": "form-control"}
        ),
        label="New Post",
    )
