from django.shortcuts import render
from django import forms
from markdown2 import Markdown

from . import util

markdowner = Markdown()

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
            "title": title,
            "entries": util.get_entry(title),
            "convert": markdowner.convert(entries)
    })

# Find entry in search bar. If query does not match, show search results 
# Clicking an entry in the search results screen will take them to the page
def search(request):
    
    # Make all entries lowercase
    entries = [entry.lower() for entry in util.list_entries()]

    # Empty list for search results that contains substring
    results = list()

    # Get term from search bar
    term = request.GET.get('q')

    # If search term is found in the entries, show entry
    if term.lower() in entries:
        print(term),
        return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(term)
    })

    # For each entry in list of entries
    for entry in entries:

    # If substring is found in entry
        if term in entry:

    # Add to results list
            results.append(entry)

    # Go to Search page with results
            return render(request, "encyclopedia/search.html", {
                "search": term,
                "entries": results
                })
    else:
    
    # No page found placeholder
        return render(request, "encyclopedia/pagenotfound.html", {
            "entries": util.get_entry(search_term)
    })
           

