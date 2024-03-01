from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = markdown_change(title)
 
    if entry is None:
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
            return redirect("entry", title=query)
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "query": query
            })
        

def create_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST["title"].upper()
        content = request.POST["content"]

        if not title:
            return render(request, "encyclopedia/create.html", {
                "error": "Title is required"
            })

        entry = util.get_entry(title)
        if entry is not None:
            return render(request, "encyclopedia/error.html", {
                "error2": "already exists.",
                "title": title
            })
        else:
            util.save_entry(title, content)
            return redirect("entry", title=title)

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
    return redirect("entry", title=title)

    
def rand(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    entry = util.get_entry(random_title)
    return redirect("entry", title=random_title)


def markdown_change(title):
    content = util.get_entry(title)
    if content is None:
        return None
    
    if title == "MAPLE":
        content_with_image = f"{content}\n\n![maple](/static/images/maple.jpg)"
        markdowner = Markdown()
        return markdowner.convert(content_with_image)
    else:
        markdowner = Markdown()
        return markdowner.convert(content)