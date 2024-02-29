from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "error": "does not exist.",
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title.upper()
        })
    
def search(request):
    if request.method == "POST":
        query = request.POST['q']
        
        entry = util.get_entry(query)
        if entry != None:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "title": query.upper()
            })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
        

def create_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        entry = util.get_entry(title)
        if entry is not None:
            return render(request, "encyclopedia/error.html", {
                "error2": "already exists.",
                "title": title
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": util.get_entry(title),
                "title": title.upper()
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['edit']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    title = request.POST["title"]
    content = request.POST["content"]
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    # content = ' '.join(content.split())

    util.save_entry(title, content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": content
    })


def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    entry = util.get_entry(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry
    })