from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ContactForm
from notes.forms import NoteForm  # noqa
from notes.models import Tag, Note  # noqa

from .models import Contact


# Create your views here.
def main(request):
    return render(request, 'contacts/index.html')


"""
Contacts
"""


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='contacts:main')
        else:
            return render(request, 'contacts/contact.html', {'form': form})

    return render(request, 'contacts/contact.html', {'form': ContactForm()})


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

            contact = Contact.objects.create(
                fullname=fullname,
                address=address,
                phone=phone,
                email=email,
                birthday=birthday,
            )

            return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/add_contact.html", context={"form": form})


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        contact.delete()
        return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/delete_contact.html", context={"contact": contact})


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        contact_form = ContactForm(request.POST, instance=contact)
        if contact_form.is_valid():
            contact_form.save()
        return redirect(reverse("contacts:my_contacts"))
    return render(request, "contacts/edit_contact.html", context={"contact": contact})


def my_contacts(request):
    contacts = Contact.objects.all()  # noqa
    fullname = request.GET.get('fullname')
    if fullname:
        contacts = contacts.filter(fullname__icontains=fullname)
    return render(request, "contacts/my_contacts.html", context={"contacts": contacts})


"""
Notes
"""


def note(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='contacts:main')
        else:
            return render(request, 'contacts/note.html', {"tags": tags, 'form': form})

    return render(request, 'contacts/note.html', {"tags": tags, 'form': NoteForm()})


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
            return redirect(to="contacts:main")
    return render(request, "contacts/add_note.html", context={"form": form})


def my_notes(request):
    notes = Note.objects.all()  # noqa
    tag = request.GET.get('tag')
    if tag:
        notes = notes.filter(tags__name__icontains=tag)
    top_tags = Tag.objects.annotate(count=Count('name')).order_by('-count')[:10]
    return render(request, "contacts/my_notes.html", context={"notes": notes, "top_tags": top_tags})
