from django.shortcuts import render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
         return render(request, "encyclopedia/error.html", {
            "error": f'Error: "{title.upper()}" - Entry not found'
        })
    else:     
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title)) 
        })
    
def search(request):
    query_title = request.GET.get('q', '')
    substring = [entry for entry in util.list_entries() if query_title.lower() in entry.lower()]
    if util.get_entry(query_title) is not None:
        return render(request, "encyclopedia/entry.html",{
            "title": query_title,
            "entry": markdown2.markdown(util.get_entry(query_title))
        })
    
    elif substring:
        return render(request, "encyclopedia/substring.html", {
            "substring": substring,
            "entry_search": query_title
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "error": f'Error: "{query_title.upper()}" - Entry not found'
        })
    
def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "error": f'Error: "{title}" - Entry already exists'
                })
        else:
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(util.get_entry(title))
            })
    else:
        return render(request, "encyclopedia/new_page.html")
    
def edit_page(request, title):
    if request.method == 'GET':
        entry = util.get_entry(title)
        # if entry is None:
        #     return render (request, "encyclopedia/error.html", {
        #         "error": f'Error - "{title}" not found'
        #     })
        if title in util.list_entries():
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "entry": entry
            })
        else:
            return render (request, "encyclopedia/error.html", {
                "error": f'Error - "{title}" not found'
            })

    elif request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(title,content)
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(entry)
            })
    
def random_page(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title))
    })