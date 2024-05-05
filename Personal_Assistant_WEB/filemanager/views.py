from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
import cloudinary
import cloudinary.uploader
import os
from .forms import FileUploadForm, CategoryForm
from .models import File
from .models import Category
from Personal_Assistant_WEB.settings import env  # noqa

cloudinary.config(cloud_name=env('CLOUD_NAME'), api_key=env('CLOUD_API_KEY'), api_secret=env('CLOUD_API_SECRET'))


@login_required
def my_files(request):
    files = File.objects.filter(user=request.user)

    if request.GET.get('search'):
        query = request.GET.get('search')

        files = files.filter(
            Q(name__icontains=query)
        )

    items_per_page = 20
    paginator = Paginator(files, items_per_page)

    page = request.GET.get("page")

    try:
        files_page = paginator.page(page)
    except PageNotAnInteger:
        files_page = paginator.page(1)
    except EmptyPage:
        files_page = paginator.page(paginator.num_pages)

    page_range = range(1, files_page.paginator.num_pages + 1)

    categories = Category.objects.filter(user=request.user)
    return render(request, 'filemanager/my_files.html',
                  {'page_title': 'Your uploaded files', 'files': files_page, 'categories': categories,
                   "page_range": page_range})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            file_to_upload = request.FILES['file']
            file_extension = os.path.splitext(file_to_upload.name)[1].lower()

            # Handling file uploads based on their extensions
            if file_extension in ['.mov', '.mp4', '.avi', '.mkv', '.wmv']:  # Video upload
                # Upload to Cloudinary
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="video",
                    folder="uploads/videos/"
                )
                file_url = uploaded_file['secure_url']

            elif file_extension in ['.jpeg', '.jpg', '.png']:  # Image upload
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="image",
                    folder="uploads/images/"
                )
                file_url = uploaded_file['secure_url']

            elif file_extension in ['.pdf', '.docx', '.xlsx']:  # Document upload
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="auto",
                    folder="uploads/documents/"
                )
                file_url = uploaded_file['secure_url']

            elif file_extension in ['.mp3', '.wav']:  # Audio upload
                uploaded_file = cloudinary.uploader.upload(
                    file_to_upload,
                    resource_type="auto",
                    folder="uploads/audio/"
                )
                file_url = uploaded_file['secure_url']

            else:
                error_message = "Invalid file format. Please upload a video file (MOV, MP4, AVI, MKV, WMV), " \
                                "image file (JPEG, JPG, PNG), document (PDF, DOCX, XLSX) or audio file (MP3, WAV)."
                # Pass form and error message to the template
                return render(request, 'filemanager/add_file.html', {'form': form, 'error_message': error_message})

            # Creating a new file object in the Django model with the Cloudinary URL
            file_instance = File.objects.create(
                user=request.user,
                url=file_url,
                name=file_to_upload.name,
            )

            # Saving the category if selected in the form
            if form.cleaned_data['category']:
                file_instance.category = form.cleaned_data['category']
            else:
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    # Creating a new category
                    category = Category.objects.create(name=new_category, user=request.user)
                    file_instance.category = category

            # Save the file instance after assigning the category
            file_instance.save()

            return redirect('filemanager:my_files')
    else:
        form = FileUploadForm(user=request.user)

    return render(request, 'filemanager/add_file.html', {'page_title': 'Upload File', 'form': form})


@login_required
def files_by_categories(request, category_id):
    files = File.objects.filter(category_id=category_id)

    items_per_page = 20
    paginator = Paginator(files, items_per_page)

    page = request.GET.get("page")

    try:
        files_page = paginator.page(page)
    except PageNotAnInteger:
        files_page = paginator.page(1)
    except EmptyPage:
        files_page = paginator.page(paginator.num_pages)

    page_range = range(1, files_page.paginator.num_pages + 1)

    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'filemanager/my_files.html',
                  {'page_title': f'Files by "{category.name}"', 'files': files_page, 'categories': categories,
                   "page_range": page_range})


@login_required
def download_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)
    try:
        with default_storage.open(file_instance.file.name) as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


@login_required
def edit_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        form = FileUploadForm(request.user, request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            form.save()
            return redirect('filemanager:my_files')
    else:
        form = FileUploadForm(request.user, instance=file_instance)
    return render(request, 'filemanager/add_file.html',
                  {'page_title': 'Edit File', 'form': form, 'file': file_instance})


@login_required
def delete_file(request, pk):
    file_instance = get_object_or_404(File, pk=pk)
    file_url = file_instance.url

    if request.method == 'POST':
        file_instance.delete()
        if file_url:
            try:
                # Отримуємо public_id з URL-адреси відео на Cloudinary
                public_id = file_url.split('/')[-1].split('.')[0]
                # Видаляємо файл з Cloudinary за public_id
                cloudinary.uploader.destroy(public_id)
            except cloudinary.exceptions.Error as e:
                print(f'Failed to delete file from Cloudinary: {e}')
        return redirect('filemanager:my_files')

    return render(request, 'filemanager/delete_file.html',
                  context={'page_title': 'Delete File',
                           "form_action": reverse("filemanager:delete_file", args=[file_instance.pk]),
                           "back_list": reverse("filemanager:my_files"),
                           'type': 'file',
                           'name': file_instance.name
                           })


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('filemanager:my_files')
    else:
        form = CategoryForm()
    uncategorized, created = Category.objects.get_or_create(name='Miscellaneous ', user=request.user,
                                                            defaults={'name': 'Miscellaneous'})
    return render(request, 'filemanager/create_category.html', {'page_title': 'Create Category', 'form': form})


@login_required
def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'filemanager/manage_categories.html',
                  {'page_title': 'Manage Categories', 'categories': categories})


@login_required
def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('filemanager:manage_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'filemanager/create_category.html',
                  {'page_title': 'Edit Category', 'category': category, 'form': form})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        uncategorized = Category.objects.filter(name='Без категорії', user=request.user).first()
        files = File.objects.filter(category=category)
        files.update(category=uncategorized)
        category.delete()
        return redirect('filemanager:manage_categories')

    return render(request, 'filemanager/delete_file.html',
                  context={'page_title': 'Delete Category',
                           "form_action": reverse("filemanager:delete_category", args=[category.pk]),
                           "back_list": reverse("filemanager:manage_categories"),
                           'type': 'category',
                           'name': category.name
                           })
