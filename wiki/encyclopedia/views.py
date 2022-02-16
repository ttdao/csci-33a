from django.shortcuts import render
from django import forms

from . import util

# Homepage shows all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Shows entry if exists. Shows a different page if 404
def entry(request, title):
    if  not(util.get_entry(title)):
        return render(request, "encyclopedia/pagenotfound.html")
    else:        
        return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(title)
    })

# Class to create form instance
class SearchTerm(forms.Form)
    term = forms.CharField(label="Search Term")

# Find entry in search bar. If query does not match, show search results 
# Clicking an entry in the search results screen will take them to the page
def search(request):
    entries = util.list_entries()

    # If method is POST
    if request.method == "POST":

        # Take in client-side search term
        term = SearchTerm(request.post)

        # Check if it exists on server-side
        if form.is_valid():

        # Go to page with search term
        return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(term)
            })
    
    
    else:

    # Take term as substring
    # Compare to each entry in list of entries - look at python lesson
    # Display all relevant entries in results.html 
           

