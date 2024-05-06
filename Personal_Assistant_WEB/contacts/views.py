import cloudinary.uploader

from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ContactForm
from notes.forms import NoteForm  # noqa
from notes.models import Tag, Note  # noqa

from .models import Contact

from datetime import date, timedelta

from news.views import news_view  # noqa

from django.contrib.auth.decorators import login_required

from Personal_Assistant_WEB.settings import env  # noqa

cloudinary.config(cloud_name=env('CLOUD_NAME'), api_key=env('CLOUD_API_KEY'), api_secret=env('CLOUD_API_SECRET'))


@login_required
def my_contacts(request):
    contacts = Contact.objects.filter(user=request.user).all() if request.user.is_authenticated else []  # noqa
    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(
            Q(fullname__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query)
        )
    return render(request, 'contacts/my_contacts.html', {"contacts": contacts, "query": query})


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
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30
    upcoming = []
    contacts = Contact.objects.filter(user=request.user).all()

    for contact in contacts:
        next_birthday = contact.birthday.replace(year=current_date.year)
        if next_birthday < current_date:
            next_birthday = next_birthday.replace(year=current_date.year + 1)

        to_date = current_date + timedelta(days=days)

        if current_date < next_birthday <= to_date:
            if next_birthday.year == current_date.year:
                turning_age = current_date.year - contact.birthday.year
            else:
                turning_age = current_date.year - contact.birthday.year + 1
            days_left_till_birthday = (next_birthday - current_date).days
            upcoming.append((contact, turning_age, days_left_till_birthday))

    upcoming = sorted(upcoming, key=lambda x: x[2])

    return render(request, "contacts/upcoming_birthdays.html", context={"upcoming": upcoming, "days": days})