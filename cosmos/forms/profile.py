import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from cosmos.models.user import Profile


def _member_clean_username(username):
    """
    Common form cleaning function for member creations and upates

    :param username: Given username to be tested
    :return: username as TUe email
    :raise ValidationError:
    """
    if User.objects.filter(username=username).exists():
        raise ValidationError(
            "There is already a user with this email in our system, please try with a different one.",
            code="duplicate_user",
        )
    if not re.search("([@.])tue.nl$", username):
        # Ensures email is from TUe (endswith ".tue.nl" or "@tue.nl"
        raise ValidationError("This field must be a valid TU/e email address", code="nontue_email")
    # Cleaning requires a return
    return username


class MemberCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def clean_username(self):
        return _member_clean_username(self.cleaned_data.get("username"))


class MemberUpdateForm(UserChangeForm):
    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_username(self):
        return _member_clean_username(self.cleaned_data.get("username"))


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nationality", "department", "program"]

    def save(self, user_ref):
        self.instance.user = user_ref
        return super().save()


class ProfileUpdateForm(ProfileCreateForm):
    class Meta:
        model = Profile
        fields = [
            "nationality",
            "department",
            "program",
            "tue_id",
            "card_number",
            "status",
            "key_access",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["status"].disabled = True
        self.fields["key_access"].disabled = True
