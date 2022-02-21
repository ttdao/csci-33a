from django.shortcuts import render, reverse
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
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="")



# Homepage shows all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Shows entry if exists. If not, show "Page Not Found"
def entry(request, title):
    if not (util.get_entry(title)):
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
        entry = util.get_entry(title)
        entry_markdown = md.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry_markdown,
        })


# Find entry in search bar. If query does not match, show search results
# Clicking an entry in the search results will take them to the page
def search(request):
    search_entries = [entry.lower() for entry in util.list_entries()]
    entries = util.list_entries()
    search_results = list()

    # Get term from search bar
    term = request.GET.get('q', '')

    # If search term is found in the entries, show entry
    if term.lower() in search_entries:
        search_entry = util.get_entry(term)
        entry_markdown = md.convert(search_entry)
        return render(request, "encyclopedia/entry.html", {
            "title": term,
            "content": entry_markdown,
        })

    # For each entry in list of entries,
    # if substring is found then add to the search results
    for search_entry in entries:
        # If substring is found in entry
        if term.lower() in search_entry.lower():
            # Add to the results list
            results.append(search_entry)
    # If the results list is populated
    if search_results:
        # for each match in the results list
        for match in search_results:
            # Go to Search page with results
            return render(request, "encyclopedia/search.html", {
                "search": term,
                "entry": match,
                "entries": search_resultsresults,
            })
    else:
        # Show No Results page
        return render(request, "encyclopedia/error.html", {
            "message": f"Could not find results for '{ term }'",
        })


# Create New Page
def new(request):
    # Retrieve list of entries
    entries = [entry.lower() for entry in util.list_entries()]

    # Check if method is post
    if request.method == "POST":

        # Take in data and save as form
        new_entry = CreateNewPage(request.POST)

        # Check if form is valid
        if new_entry.is_valid():

            # Get the title
            title = new_entry.cleaned_data["title"]

            # Get the content
            content = new_entry.cleaned_data["content"]

            # If title already exists, go to error page
            if title.lower() in entries:
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "message": f"The '{title}' page already exists! Please edit the entry instead!"
                })

            #  Otherwise, save new title and content
            else:
                util.save_entry(title, content)

                # Go to newly created page
                return HttpResponseRedirect(reverse('encyclopedia:title', args=(title, )))

        # if form is INVALID, re-render the page with existing information
        else:
            return render(request, "encyclopedia/new.html", {
                "form": new_entry,
            })

    # If method is GET, go to create new page
    else:
        return render(request, "encyclopedia/new.html", {
            "form": CreateNewPage()
        })


# Go to random page
def rand(request):
    # Get list of entries
    entries = util.list_entries()

    # Pick number between 0 and length of entries list
    rng = random.randint(0, len(entries) - 1)

    # Store title
    random_title = entries[rng]

    # Redirect to random entry
    return HttpResponseRedirect(reverse('encyclopedia:title', args=(random_title, )))


# Edit existing entry
def edit(request, title):

    # Check to see if method is GET
    if request.method == "GET":

        # Get the entry content
        edit_content = util.get_entry(title)

        if edit_content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "Oops, you're trying to edit a non-existent entry. Create a new one!"
            })

        # Pre-populate page with initial title and content
        edit_form = EditPage(initial={'title': title, 'content': edit_content})

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": edit_form,
        })

    else:

        # When it is POST
        edit_form = EditPage(request.POST)

        # Check if form data is valid (server-side)
        if edit_form.is_valid():
            # Isolate the content from the 'cleaned' version of form data
            title = edit_form.cleaned_data["title"]

            # Isolate the content from the 'cleaned' version of form data
            content = edit_form.cleaned_data["content"]

            # Call util to store data
            util.save_entry(title, content)

            # Redirect to edited entry
            return HttpResponseRedirect(reverse('encyclopedia:title', args=(title, )))

    # if INVALID, reload the page
    return render(request, "encyclopedia/edit.html", {
        "edit": EditPage(initial={'title': title, 'content': util.get_entry(title)}),
    })
