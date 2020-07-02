from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewPageEntry(forms.Form):
    page = forms.CharField(label="New Page")


def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })


def add(request):
    if request.method == "POST":
        form = NewPageEntry(request.POST)
        if form.is_valid():
            page = form.cleaned_data["Pwiki"]
            request.session["Pwiki"] += [page]
            return HttpResponseRedirect(reverse("Pwiki:index"))
        else:
            return render(request, "Pwiki/NewPage.html", {
                "form": form
            })
    else:
        return render(request, "Pwiki/NewPage.html", {
            "form": NewPageEntry()
        })
