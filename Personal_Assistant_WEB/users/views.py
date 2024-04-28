from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegistrationForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="contacts:main")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Registration of {username} has been successfully completed.")
            return redirect(to="users:signin")
        return render(request, self.template_name, context={"form": form})
