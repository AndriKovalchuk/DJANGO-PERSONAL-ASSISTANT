import os
import cloudinary
import cloudinary.uploader

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProfileForm, AvatarUploadForm
from .models import Profile
from users.forms import UserEditForm  # noqa
from Personal_Assistant_WEB.settings import env  # noqa

cloudinary.config(cloud_name=env('CLOUD_NAME'), api_key=env('CLOUD_API_KEY'), api_secret=env('CLOUD_API_SECRET'))


@login_required
def my_profile(request, profile_name):
    user = request.user
    profile = user.profile
    return render(request, 'profiles/my_profile.html', {'profile': profile})


@login_required
def edit_profile(request, profile_name):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profiles:my_profile', profile_name=profile_name)
        else:
            print(f"USER ERRORS: {user_form.errors}")
            print(f"PROFILE ERRORS: {profile_form.errors}")
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'profile': profile})


@login_required
def upload_avatar(request, profile_name):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = AvatarUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            avatar_to_upload = request.FILES['file']
            avatar_extension = os.path.splitext(avatar_to_upload.name)[1].lower()

            # Handling file uploads based on their extensions
            if avatar_extension in ['.png', '.jpg', '.jpeg']:
                # Upload to Cloudinary
                uploaded_image = cloudinary.uploader.upload(
                    avatar_to_upload,  # Corrected the file object
                    resource_type="image",
                    folder="uploads/images/avatars/"
                )
                image_url = uploaded_image['secure_url']

                # Creating a new file object in the Django model with the Cloudinary URL
                profile.avatar = avatar_to_upload
                profile.save()

                return redirect('profiles:edit_profile', profile_name=profile_name)

            else:
                error_message = "Invalid file format. Please upload an image file (JPEG, JPG, PNG)"
                return render(request, 'profiles/upload_avatar.html', {'form': form, 'error_message': error_message})

        else:
            print(f"UPLOAD ERRORS: {form.errors}")
    else:
        form = AvatarUploadForm(user=request.user)

    return render(request, 'profiles/upload_avatar.html', {'form': form})
