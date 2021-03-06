from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.users.factory import get_newsletter_service
from apps.users.forms import MemberCreateForm, MemberUpdateForm, ProfileCreateForm, ProfileUpdateForm

newsletter_service = get_newsletter_service()


def register(request):
    """
    Process User registration form

    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = MemberCreateForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            profile_form = ProfileCreateForm(request.POST, instance=user.profile)

            user.profile = profile_form.save(user)
            messages.success(request, "Account created successfully")

            # Log in automatically
            raw_password = user_form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("/")

        else:
            profile_form = ProfileCreateForm(request.POST)
    else:
        user_form = MemberCreateForm()
        profile_form = ProfileCreateForm()
    return render(request, "user/register.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
@transaction.atomic
def process_profile_form(request):
    """
    Process User profile form.

    - @login_required: Ensures authenticated user
    - @transaction.atomic: Ensures both queries to the database are transactions

    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = MemberUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(data=request.POST, instance=request.user.profile)
        password_form = PasswordChangeForm(data=request.POST, user=request.user)

        if "save_profile" in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile was successfully updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#profile")
        elif "save_password" in request.POST:
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Your password was succesfully updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#password")
        elif "save_preferences" in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your preferences were succesfully updated!")
                return redirect(request("cosmos_users:user_profile") + "#preferences")
        elif "save_key_access" in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your key access settings were succesfully updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#key-access")

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = MemberUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
    return render(
        request,
        "user/profile.html",
        {"user_form": user_form, "profile_form": profile_form, "password_form": password_form},
    )


@login_required
def delete(request):
    if request.method == "POST":
        # Remove newsletter subscription before deleting the user
        newsletter_service.remove_subscription(request.user.username)
        newsletter_service.remove_subscription(request.user.email)
        User.objects.get(username=request.user.username).delete()
    return redirect("/")
