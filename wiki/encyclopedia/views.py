from django.shortcuts import render

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
