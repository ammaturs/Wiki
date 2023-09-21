from django.shortcuts import render, redirect
from markdown2 import Markdown
import markdownify
from . import util
from django.contrib import messages
import random


def index(request):
    if request.method == "POST":
        search_q = str(request.POST["q"])
        sub_list=[]

        #list of all our entries
        entrys = util.list_entries()

        #loop through wiki entries, if in return
        for entry in entrys:
            if search_q.lower() == entry.lower():
                return redirect("page", page=entry)
            else:
                #is it a substring?
                if search_q.lower() in entry.lower():
                    sub_list.append(entry)

        #if we made it here, search query didnt match any pages. Take user to search results page that displays a list of all encyclopedia entries that have the query as a substring.

        return render(request, "encyclopedia/search.html", {"search":search_q, "sub_list": sub_list})

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries() #list_entries() returns a list of the names of all encyclopedia entries currently saved
        })

#page argument is the user input in the url i.e what comes after the / i.e their wiki search

def page(request, page):
    markdowner = Markdown()
    md = util.get_entry(page)

    if md == None:
        return render(request, "encyclopedia/error.html")

    else:
        #markdown to html
        contents = markdowner.convert(md)

        return render(request, "encyclopedia/page.html", {"title":page, "contents":contents})

def create(request):
    if request.method == "POST":

        #list of all our entries
        entrys = util.list_entries()

        title = str(request.POST["title"])
        markdown = request.POST["markdown"]
       

        #if entry already exists, user should be presented with an error message
        for entry in entrys:
            if title.lower() == str(entry.lower()):

                #redirect to same page with error message
                messages.error(request,'Wiki page already exists.')
                return redirect('create')

        #create an md file and write the contents to it appropriately
        util.save_entry(title, markdown)
        return redirect('page', page=title) #redirects to specified view function

    else:
        return render(request, "encyclopedia/create.html")


def edit(request):
    #edit was saved, overwrite existing/old md file
    if request.method == "POST":
        title = str(request.POST["title"])
        markdown = (request.POST["markdown"]).strip()
        util.save_entry(title, markdown)
        return redirect('page', page=title)


    #Pass title and markdown content of page we want to edit
    else:
        title = request.GET.get("title")
        contents = util.get_entry(title)

        markdowner = Markdown()
        contents_html = markdowner.convert(contents)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "contents":contents
        })

def randompage(request):
    entries = util.list_entries()
    return redirect('page', page=random.choice(entries))
