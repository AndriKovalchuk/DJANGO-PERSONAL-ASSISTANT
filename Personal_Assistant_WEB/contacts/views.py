import os

import cloudinary
import cloudinary.uploader
import requests
from django.db.models import Count, Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse

from .forms import ContactForm
from notes.forms import NoteForm  # noqa
from notes.models import Tag, Note  # noqa

from .models import Contact

from datetime import date, timedelta

from news.views import news_view  # noqa

from django.contrib.auth.decorators import login_required

from Personal_Assistant_WEB.settings import env  # noqa

cloudinary.config(cloud_name=env('CLOUD_NAME'), api_key=env('CLOUD_API_KEY'), api_secret=env('CLOUD_API_SECRET'))


# Create your views here.
def main(request):
    return news_view(request)


"""  
Contacts
"""


@login_required
def my_contacts(request):
    contacts = Contact.objects.filter(user=request.user).all() if request.user.is_authenticated else []  # noqa
    return render(request, "contacts/my_contacts.html", context={"contacts": contacts})


@login_required
def add_contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()

            return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/add_contact.html", context={"form": form})


@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(reverse("contacts:my_contacts"))
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/edit_contact.html", context={"contact": contact, "form": form})


@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == "POST":
        contact.delete()
        return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/delete_contact.html", context={"contact": contact})


@login_required
def upcoming_birthdays(request):
    current_date = date.today()
    to_date = current_date + timedelta(days=7)
    upcoming = []
    contacts = Contact.objects.filter(user=request.user).all()  # noqa

    for contact in contacts:

        contact_birthday_month_day = (contact.birthday.month, contact.birthday.day)
        current_date_month_day = (current_date.month, current_date.day)
        to_date_month_day = (to_date.month, to_date.day)

        if current_date_month_day < contact_birthday_month_day <= to_date_month_day:
            turning_age = current_date.year - contact.birthday.year
            days_left_till_birthday = contact_birthday_month_day[1] - current_date_month_day[1]
            upcoming.append((contact, turning_age, days_left_till_birthday))

    upcoming = sorted(upcoming, key=lambda x: x[2])

    return render(request, "contacts/upcoming_birthdays.html", context={"upcoming": upcoming})


@login_required
def search_results_contacts(request):
    contacts = Contact.objects.filter(user=request.user).all()  # noqa
    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(Q(fullname__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
        for el in contacts:
            print(el.fullname)
    return render(request, 'contacts/search_results_contacts.html', {"contacts": contacts, "query": query})


"""
Notes
"""


@login_required
def my_notes(request):
    notes = Note.objects.filter(user=request.user).all()  # noqa
    tag = request.GET.get('tag')
    if tag:
        notes = notes.filter(tags__name__icontains=tag)
    top_tags = Tag.objects.filter(note__user=request.user).annotate(count=Count('note')).order_by('-count')[:10]
    return render(request, "contacts/my_notes.html", context={"notes": notes, "top_tags": top_tags})


@login_required
def add_note(request):
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            description = form.cleaned_data['description']
            tags_input = form.cleaned_data['tags']

            new_note = Note.objects.create(
                text=text,
                description=description,
                user=request.user,
            )
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                new_note.tags.add(tag)
            return redirect(reverse("contacts:my_notes"))
    return render(request, "contacts/add_note.html", context={"form": form})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            text = form.cleaned_data['text']
            description = form.cleaned_data['description']
            tags_input = form.cleaned_data['tags']

            note.text = text
            note.description = description
            note.save()

            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            existing_tags = note.tags.all()

            for tag in existing_tags:
                if tag.name not in tags_list:
                    note.tags.remove(tag)

            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                note.tags.add(tag)

            Tag.objects.filter(note=None).delete()

            return redirect("contacts:my_notes")
    else:
        form = NoteForm(instance=note)
    return render(request, "contacts/edit_note.html", {"form": form, "note": note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        tags_to_delete = list(note.tags.all())
        note.delete()
        for tag in tags_to_delete:
            if tag.note_set.count() == 0:
                tag.delete()
        return redirect(reverse("contacts:my_notes"))
    return render(request, "contacts/delete_note.html", context={"note": note})


@login_required
def search_results_notes(request):
    notes = Note.objects.filter(user=request.user).all()  # noqa
    query = request.GET.get('q')
    if query:
        notes = notes.filter(Q(text__icontains=query) | Q(tags__name__icontains=query))
    return render(request, 'contacts/search_results_notes.html', {'notes': notes, 'query': query})
