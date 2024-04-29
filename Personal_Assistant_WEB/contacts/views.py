import os

import cloudinary
import cloudinary.uploader
import requests
from django.db.models import Count, Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .forms import ContactForm, UploadFileForm
from notes.forms import NoteForm  # noqa
from notes.models import Tag, Note  # noqa

from .models import Contact, File

from datetime import date, timedelta

from news.views import news_view  # noqa

cloudinary.config(cloud_name='andriikovalchuk', api_key='987726452543244', api_secret='4vmOFEveTcjTYiN_dwnTUBKZVbA')


# Create your views here.
def main(request):
    return news_view(request)


"""
Contacts
"""


def my_contacts(request):
    contacts = Contact.objects.all()  # noqa
    return render(request, "contacts/my_contacts.html", context={"contacts": contacts})


def add_contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            birthday = form.cleaned_data['birthday']

            contact = Contact.objects.create(  # noqa
                fullname=fullname,
                address=address,
                phone=phone,
                email=email,
                birthday=birthday,
            )

            return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/add_contact.html", context={"form": form})


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        contact_form = ContactForm(request.POST, instance=contact)
        if contact_form.is_valid():
            contact_form.save()
        return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/edit_contact.html", context={"contact": contact})


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        contact.delete()
        return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/delete_contact.html", context={"contact": contact})


def upcoming_birthdays(request):
    current_date = date.today()
    to_date = current_date + timedelta(days=7)
    upcoming = []
    contacts = Contact.objects.all()  # noqa

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


def search_results_contacts(request):
    contacts = Contact.objects.all()
    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(Q(fullname__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
        for el in contacts:
            print(el.fullname)
    return render(request, 'contacts/search_results_contacts.html', {"contacts": contacts, "query": query})


"""
Notes
"""


def my_notes(request):
    notes = Note.objects.all()  # noqa
    tag = request.GET.get('tag')
    if tag:
        notes = notes.filter(tags__name=tag)
    top_tags = Tag.objects.annotate(count=Count('note')).order_by('-count')[:10]
    return render(request, "contacts/my_notes.html", context={"notes": notes, "top_tags": top_tags})


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
            )
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                new_note.tags.add(tag)
            return redirect(reverse("contacts:my_notes"))
    return render(request, "contacts/add_note.html", context={"form": form})


def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
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


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        tags_to_delete = list(note.tags.all())
        note.delete()
        for tag in tags_to_delete:
            if tag.note_set.count() == 0:
                tag.delete()
        return redirect(reverse("contacts:my_notes"))
    return render(request, "contacts/delete_note.html", context={"note": note})


def search_results_notes(request):
    notes = Note.objects.all()  # noqa
    query = request.GET.get('q')
    if query:
        notes = notes.filter(Q(text__icontains=query) | Q(tags__name__icontains=query))
    return render(request, 'contacts/search_results_notes.html', {'notes': notes, 'query': query})


"""
Files
"""


def my_files(request):
    files = File.objects.all()  # noqa
    return render(request, 'contacts/my_files.html', {'files': files})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_to_upload = request.FILES['file']
            file_extension = os.path.splitext(file_to_upload.name)[1].lower()
            # video upload
            if file_extension in ['.mov', '.mp4', '.avi', '.mkv', '.wmv']:
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="video",
                    folder="uploads/videos/"
                )
                file_url = uploaded_file['secure_url']
                file_object = File.objects.create(
                    url=file_url,
                    name=file_to_upload.name
                )
                return redirect(reverse("contacts:my_files"))
            # image upload
            elif file_extension in ['.jpeg', '.jpg', '.png']:
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="image",
                    folder="uploads/images/"
                )
                file_url = uploaded_file['secure_url']
                file_object = File.objects.create(
                    url=file_url,
                    name=file_to_upload.name
                )
                return redirect(reverse("contacts:my_files"))
            # document upload
            elif file_extension in ['.pdf', '.docx', '.xlsx']:
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="auto",
                    folder="uploads/documents/"
                )
                file_url = uploaded_file['secure_url']
                file_object = File.objects.create(
                    url=file_url,
                    name=file_to_upload.name
                )
                return redirect(reverse("contacts:my_files"))

            # audio upload
            elif file_extension in ['.mp3', '.wav']:
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="auto",
                    folder="uploads/audio/"
                )
                file_url = uploaded_file['secure_url']
                file_object = File.objects.create(
                    url=file_url,
                    name=file_to_upload.name
                )
                return redirect(reverse("contacts:my_files"))
            else:
                error_message = "Invalid file format. Please upload a video file (MOV, MP4, AVI, MKV, WMV), image file (JPEG, JPG, PNG), document (PDF, DOCX, XLSX) or audio file (MP3, WAV)."
                return render(request, 'contacts/upload_file.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadFileForm()

    return render(request, 'contacts/upload_file.html', {'form': form})


def download_file(request, file_url):
    file_name = file_url.split('/')[-1]  # get the filename from the URL
    response = requests.get(file_url, stream=True)  # get the file content from Cloudinary

    if response.status_code == 200:
        # Set the Content-Disposition header to force download
        response = HttpResponse(response.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    else:
        return HttpResponse("File not found", status=response.status_code)
