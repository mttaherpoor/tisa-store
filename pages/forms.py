from django import forms
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your name')
        }),
        label=_("Name")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your email')
        }),
        label=_("Email")
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': _('Write your message here...')
        }),
        label=_("Message")
    )
    def save(self):
        """Custom save method — e.g., send email or store in DB"""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        # Example: send email
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f'{message} and from {name} with this {email=}',
            from_email=email,
            recipient_list=['tisavista@gmail.com'],
        )
        # Or save to a model if you have ContactMessage model
        # ContactMessage.objects.create(name=name, email=email, message=message)
