from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

from markdown2 import Markdown

from . import util

class newEntryForm(forms.Form):
    entryTitle = forms.CharField(label="New Entry Title")
    entryMarkdown = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Use Markdown here :)"}))

class editEntryForm(forms.Form):
    entryMarkdown = forms.CharField(widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showEntry(request, entry):
    
    markdowner = Markdown()
    
    try:
        html = markdowner.convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "html": html
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "error": f"The entry {entry} doesn't exist!"
        })
    

def search(request):
    if request.method == "POST":

        q = request.POST["q"].lower()
        lowercase_entries = [i.lower() for i in util.list_entries()]

        if q in lowercase_entries:
             return HttpResponseRedirect(f"wiki/{q}")
        else:
            results = [i for i in util.list_entries() if q in i.lower()]
            return render(request, "encyclopedia/searchresults.html", {
                "query": request.POST["q"],
                "results": results
            })
    else:
        return HttpResponseRedirect(reverse("index"))


class newEntryForm(forms.Form):
    entryTitle = forms.CharField(label="New Entry Title")
    entryMarkdown = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Use Markdown here :)"}))


def newEntry(request):
    if request.method == "POST":
        
        form = newEntryForm(request.POST)
        
        if form.is_valid():
            newEntryTitle = form.cleaned_data["entryTitle"]
            newEntryMarkdown = form.cleaned_data["entryMarkdown"].replace("\n", "")

            if newEntryTitle not in util.list_entries():
                util.save_entry(newEntryTitle, newEntryMarkdown)
                return HttpResponseRedirect(f"wiki/{newEntryTitle}")
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": f"The entry {newEntryTitle} already exists!"
                })

    elif request.method == "GET":
        return render(request, "encyclopedia/newentry.html", {
            "form": newEntryForm()
        })


def editEntry(request, entry):
    if request.method == "POST":
       
        form = editEntryForm(request.POST)
        
        if form.is_valid():
            entryMarkdown = form.cleaned_data["entryMarkdown"].replace("\n", "")

            util.save_entry(entry, entryMarkdown)
            return HttpResponseRedirect(f"/wiki/{entry}")
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "WRONG!"
            })

    elif request.method == "GET":

        content = util.get_entry(entry)
        form = editEntryForm(initial={'entryMarkdown': content})
                
        return render(request, "encyclopedia/editEntry.html", {
            "entry": entry,
            "form": form
        })