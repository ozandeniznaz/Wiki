from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown
from . import util
from django import forms
import random

class NewEntry(forms.Form):
    entry_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            "placeholder":"Mahmut",
        }))
    entry_description = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            "placeholder":"Mahmut is a boy's name of Arabic origin. The meaning of the name Mahmut is one who is outspoken, worthy of praise or praise.",
            "name":"description",
            "rows":"3",
            "cols":"5",
        }))

class EditEntry(forms.Form):
    entry_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            "readonly":"readonly",
        }))
    entry_description = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            "name":"description",
            "rows":"3",
            "cols":"5",
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries()
    })

def md_to_html(title):
    md_file = util.get_entry(title)
    if md_file == None:
        return None     #gives TypeError error if i do not return None for None.
    else:
        html_file = markdown(md_file)
        return html_file

def entry(request, title):
    html = md_to_html(title)
    if html == None:
        entries = util.list_entries()
        related = []
        for entry_name in entries:
            if title in entry_name.lower() or entry_name.lower() in title:
                related.append(entry_name)
        return render(request, "encyclopedia/error.html", {
            "error_title" : title.capitalize() + " does not exist! - Encyclopedia",
            "error_message" : "Your entry does not exist!",
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title" : title.upper() + " - Encyclopedia",
            "content" : html,
            "title" : title,
        })

def search(request):
    term = request.POST['q']
    content = md_to_html(term)
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry_title" : term.upper() + " - Encyclopedia",
            "content" : content,
            })
    else:
        entries = util.list_entries()
        related = []
        for entry_name in entries:
            if term in entry_name.lower() or entry_name.lower() in term:
                related.append(entry_name)
        return render(request, "encyclopedia/search.html", {
            "related" : related
        })

def new_entry(request):
    form = NewEntry(request.POST or None)
    if form.is_valid():
        title = form.cleaned_data['entry_name']
        text = form.cleaned_data['entry_description']
    else:
        return render(request, "encyclopedia/new.html", {
        "new_entry_form": form,
        })
        
    if util.get_entry(title):
        return render(request, "encyclopedia/create_error.html", {
            "error":'This page title already exists! Please go to that title page and edit it instead!'
        })
    else:
        util.save_entry(title, text)
        content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "entry_title" : title.upper() + " - Encyclopedia",
            "content" : content,
            "title" : title,
            })

def edit(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "error_title" : title.capitalize() + " - Encyclopedia",
            "error_message" : "Your entry does not exist!",
            })
    else:
        form = EditEntry(request.POST or None, initial={'entry_name': title, 'entry_description': entry})
        if form.is_valid():
            text = form.cleaned_data['entry_description']
        else:
          return render(request, "encyclopedia/edit.html", {
            "edit_entry_form": form,
          })
        
    if util.get_entry(title):
        util.save_entry(title, text)
        content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "entry_title" : title.upper() + " - Encyclopedia",
            "content" : content,
            "title" : title,
            })
    else:
        util.save_entry(title, text)
        content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "entry_title" : title.upper() + " - Encyclopedia",
            "content" : content,
            "title" : title,
            })

def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect(reverse('entry', args=[entry]))