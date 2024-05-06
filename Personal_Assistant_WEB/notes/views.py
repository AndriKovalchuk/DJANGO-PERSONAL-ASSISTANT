import cloudinary.uploader
from django.db.models import Count, Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from notes.forms import NoteForm  # noqa
from notes.models import Tag, Note  # noqa

from news.views import news_view  # noqa

from django.contrib.auth.decorators import login_required

from Personal_Assistant_WEB.settings import env  # noqa

cloudinary.config(cloud_name=env('CLOUD_NAME'), api_key=env('CLOUD_API_KEY'), api_secret=env('CLOUD_API_SECRET'))


@login_required
def my_notes(request):
    notes = Note.objects.filter(user=request.user).all()  # noqa
    tag = request.GET.get('tag')
    query = request.GET.get('q')
    if tag:
        notes = notes.filter(tags__name__icontains=tag)
    if query:
        notes = notes.filter(Q(text__icontains=query) | Q(tags__name__icontains=query))
    top_tags = Tag.objects.filter(note__user=request.user).annotate(count=Count('note')).order_by('-count')[:10]
    return render(request, "notes/my_notes.html", context={"notes": notes, "top_tags": top_tags, 'query': query})


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
            return redirect(reverse("notes:my_notes"))
    return render(request, "notes/add_note.html", context={"form": form})


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

            return redirect("notes:my_notes")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/edit_note.html", {"form": form, "note": note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        tags_to_delete = list(note.tags.all())
        note.delete()
        for tag in tags_to_delete:
            if tag.note_set.count() == 0:
                tag.delete()
        return redirect(reverse("notes:my_notes"))
    return render(request, "notes/delete_note.html", context={"note": note})
