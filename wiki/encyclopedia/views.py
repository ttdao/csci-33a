from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random

from . import util

md = Markdown()


class CreateNewPage(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea(), label="content")


class EditPage(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='content')


# Homepage shows all entries
def index(request):
    # Check if there is already an existing session
    # if "entries" not in request.session:
    #     request.session["entries"] = []
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Shows entry if exists. Shows a different page if 404
def entry(request, title):
    if not (util.get_entry(title)):
        return render(request, "encyclopedia/pagenotfound.html")
    else:
        entry = util.get_entry(title)
        entry_markdown = md.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry_markdown,
        })


# Find entry in search bar. If query does not match, show search results
# Clicking an entry in the search results screen will take them to the page
def search(request):
    search_entries = [entry.lower() for entry in util.list_entries()]
    entries = util.list_entries()
    results = list()

    # Get term from search bar
    term = request.GET.get('q', '')

    # If search term is found in the entries, show entry
    if term.lower() in search_entries:
        entry = util.get_entry(term)
        entry_markdown = md.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": term,
            "content": entry_markdown,
        })
    # For each entry in list of entries,
    # if substring is found then add to the results list
    for entry in entries:
        # If substring is found in entry
        if term.lower() in entry.lower():
            # Add to the results list
            results.append(entry)
    # If the results list is populated
    if results:
        # for each match in the results list
        for match in results:
            # Go to Search page with results
            return render(request, "encyclopedia/search.html", {
                "search": term,
                "entry": match,
                "entries": results,
            })
    else:
        # Show No Results page
        return render(request, "encyclopedia/noresults.html", {
            "search": term,
        })


# Create New Page
def new(request):

    # Retrieve list of entries
    entries = util.list_entries()

    # Check if method is post
    if request.method == "POST":

        # Take in data and save as form
        form = CreateNewPage(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Get the title
            title = form.cleaned_data["title"]

            # Get the content
            content = form.cleaned_data["content"]

            # If title already exists, go to Already Exist page
            if title in entries:
                return render(request, "encyclopedia/alreadyexist.html", {
                    "title": title,
                })

            #  Otherwise, save new title and content with Save Entry util
            else:
                util.save_entry(title, content)

            # Go to newly created page
                return HttpResponseRedirect("/wiki/" + title)

        # if form is INVALID, re-render the page with existing information
        else:
            return render(request, "encyclopedia/new.html",{
                "form": form,
            })

    # If method is GET, go to create new page
    else:
        return render(request, "encyclopedia/new.html", {
            "form": CreateNewPage()
        })


def rand(request):
    # Get list of entries
    entries = util.list_entries()

    # Pick number between 0 and length of entries list
    index = random.randint(0, len(entries) - 1)

    # Store title
    random_title = entries[index]

    # Perform markdown
    entry = util.get_entry(random_title)
    entry_markdown = md.convert(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "entry": entry_markdown
    })


def edit(request, title):

    # Check to see if method is GET
    if request.method == "GET":

        # Get the title
        title = request.GET.get['title']

        # Get the entry content
        content = util.get_entry(title)

        # Pre-populate page with initial title and content
        edit = EditPage(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit": edit,
        })
    else:

        # When it is POST
        edit = EditPage(request.post)

        # Check if form data is valid (server-side)
        if edit.is_valid():

            # Isolate the title from the 'cleaned' version of form data
            title = edit.cleaned_data["title"]

            # Isolate the content from the 'cleaned' version of form data
            content = edit.cleaned_data["content"]

            # Call util to store data
            util.save_entry(title, content)

            # Redirect to list of entries
            return HttpResponseRedirect(reverse("encyclopedia:index"))
