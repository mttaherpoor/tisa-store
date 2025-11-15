from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from accounts.validators import validate_file_size

from .models import CustomUser, Ticket

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()

        fields = ('email', 'username', )


class ProfileForm(forms.ModelForm):
    # اضافه کردن محدودیت حجم فایل به فیلد avatar / profile_image
    profile_image = forms.ImageField(required=False, validators=[validate_file_size])

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "profile_image"]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["subject", "message"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
