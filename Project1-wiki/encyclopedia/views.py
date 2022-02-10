from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from .forms import EditPageForm, NewPageFrom

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_name:str):
    entry = util.get_entry(entry_name)
    html_entry = ""
    if entry is not None:
        html_entry = str(util.Markdown(entry))
    
    return render(request, "encyclopedia/entry.html", {
        "entry" : html_entry,
        "title" : entry_name
    })


def search(request):
    query:str = request.GET.get("q", "")
    all_entries = util.list_entries()
    if query in all_entries:
        return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[query]))
    else:
        results = [entry for entry in all_entries if entry.lower().find(query.lower()) >= 0]
        return render(request, "encyclopedia/search.html", {
            "results" : results,
            "query" : query
        })


def new_page(request):
    
    if request.method == 'POST':
        _form = NewPageFrom(request.POST)

        if _form.is_valid():
            util.save_entry(_form.cleaned_data["title"], _form.cleaned_data["text"])
            return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[_form.cleaned_data["title"]]))
    else:
        _form  = NewPageFrom()
        
    return render(request, "encyclopedia/page_edit.html", {
        "page_form" : _form,
        "page_title": "Add New Page",
        "path": "/add"
    })

def edit_page(request, entry_name):
    if request.method == "POST":
        _form = EditPageForm(request.POST)
        if _form.is_valid():
            util.save_entry(_form.cleaned_data["title"], _form.cleaned_data["text"])
            return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[_form.cleaned_data["title"]]))
    else:
        _form = EditPageForm({
            "title": entry_name,
            "text": util.get_entry(entry_name)
        })

    return render(request, "encyclopedia/page_edit.html", {
        "page_form" : _form,
        "page_title": "Edit Page",
        "path": f"/edit/{entry_name}"
    })


def random_page(request):
    all_entries = util.list_entries()
    random_entry:str = all_entries[randint(0, len(all_entries)-1)]
    return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[random_entry]))
    