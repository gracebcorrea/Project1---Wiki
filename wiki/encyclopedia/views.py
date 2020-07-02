from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    if "encyclopedia" not in request.session:
        request.session["encyclopedia"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["encyclopedia"]
    })
