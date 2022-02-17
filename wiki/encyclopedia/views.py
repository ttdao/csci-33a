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

<<<<<<< HEAD
# Class to create form instance
#class SearchTerm(forms.Form):
#   term = forms.CharField(label="Search Term")

# Find entry in search bar. If query does not match, show search results 
# Clicking an entry in the search results screen will take them to the page
def search(request):
    entries = util.list_entries()
    
    # If method is GET
    if request.method == "GET":
        search_term = request.GET.get('q')
        # Go to page with search term
        return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(search_term)
            })

    
    #else:

    # Take term as substring
    # Compare to each entry in list of entries - look at python lesson
    # Display all relevant entries in results.html 
=======
# Find entry in search bar. If query does not match, show search results 
# Clicking an entry in the search results screen will take them to the page
def search(request):

    # Lowercase all entries
    entries = [entry.lower() for entry in util.list_entries()]
    results = list()
    term = request.GET.get('q')

    # If term exist in list of entries, show page
    if term in entries:
            return render(request, "encyclopedia/entry.html", {
        "entries": util.get_entry(term)
        })

    # Find substring in each entry in entries:
    for entry in entries:
        if term in entry:
            # Add to results and then display it in results
            return render(request, "encyclopedia/results.html", {
        "entries": util.get_entry(term)
        })

        else:
            return render(request, "encyclopedia/pagenotfound.html")
             #No page found placeholder
        # Display all relevant entries in results.html 
>>>>>>> origin/SearchBox
           

