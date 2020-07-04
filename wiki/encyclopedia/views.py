from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="NewTitle")
    content = forms.CharField(label="NewContent")


def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })


#New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create
#a new encyclopedia entry.
#Users should be able to enter a title for the page and, in a textarea, should be able to enter the
#Markdown content for the page.
#Users should be able to click a button to save their new page.
#When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
#Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.

def NewPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = request.POST["NewTitle"]
            content = request.POST["NewItem"]

            request.session["Pwiki"] += [Pwiki]
            print([title], [content])

            return render(request, "encyclopedia/index.html", {
                "entries":util.save_entry(title, content),
                "encyclopedia": request.session["Pwiki"]
            })
    else:
        return render(request, "encyclopedia/NewPage.html")


#Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

def RandomPage(request):
    if request.method == "GET":
        return HttpResponse("Error. Wrong request method for Random")
    else:
        return HttpResponseRedirect(reverse("RandomPage"))

#Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be
#converted to HTML before being displayed to the user. You may use the python-markdown2 package
#to perform this conversion, installable via pip3 install markdown2.
#Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the
#Markdown to HTML conversion without using any external libraries, supporting headings, boldface text,
# unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.
def EntryPage(request):
    return (request, "encyclopedia/EntryPage.html",{"message":"Entry Page"})


#Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
#The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
#The user should be able to click a button to save the changes made to the entry.
#Once the entry is saved, the user should be redirected back to that entry’s page.

def EditPage(request):
    return (request, "encyclopedia/EditPage.html",{"message":"Edit Page"})

#New Files
def Entries(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            request.session["entries"] += [entry]
            return HttpResponseRedirect(reverse("entries:index"))
        else:
            return render(request, "entries/index.html", {
                "form": form
            })
    else:
        return render(request, "entries/index.html", {
            "form": NewEntryForm()
        })


#Search: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
#If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
#If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were Py, then Python should appear in the search results.
#Clicking on any of the entry names on the search results page should take the user to that entry’s page.
def Search():
    return ("EntryPage.html")




def AlertsDjango(request):
    return render(request, "encyclopedia/AlertsDjango.html",{"tipo":"Alert"})
