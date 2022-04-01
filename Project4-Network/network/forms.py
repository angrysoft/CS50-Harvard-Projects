from django import forms


class NewPostForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "new-post form-control"}),
        label="New Post",
    )
