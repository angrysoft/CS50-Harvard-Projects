from click import edit
from django import forms
from django.core import validators
from . import util

def validate_title(value):
    if value is None or value == "":
        raise forms.ValidationError("Value is empty or none")
    
    all_entries = util.list_entries()
    if value in all_entries:
        raise forms.ValidationError(f"Page with title {value} already exist")


class NewPageFrom(forms.Form):
    title = forms.CharField(label="Title", max_length=100, validators=[validate_title, validators.validate_slug])
    text = forms.CharField(widget=forms.Textarea())

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, validators=[validators.validate_slug])
    text = forms.CharField(widget=forms.Textarea())
