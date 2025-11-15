from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .validators import username_validator,email_validator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150,unique=True,validators=[username_validator])
    email = models.EmailField(unique=True,validators=[email_validator])
    profile_image = models.ImageField(_("Profile Image"),upload_to="accounts/profile_image/",blank=True)


class Ticket(models.Model):
    TICKET_STATUS_OPEN = 'o'
    TICKET_STATUS_IN_PROGRESS = 'p'
    TICKET_STATUS_CLOSED = 'c'
    
    TICKET_STATUS_CHOICES = [
        (TICKET_STATUS_OPEN, 'Open'),
        (TICKET_STATUS_IN_PROGRESS, 'In Progress'),
        (TICKET_STATUS_CLOSED, 'Closed'),
    ]

    SUBJECT_CHOICES = [
        ("technical", "مشکل فنی – خطا در سایت، دانلود نشدن ویدیو..."),
        ("course", "پرسش درباره‌ی دوره‌ها"),
        ("education", "درخواست پشتیبانی آموزشی"),
        ("payment", "مشکل پرداخت/مالی"),
        ("feedback", "پیشنهاد یا انتقاد"),
        ("other", "سایر موارد"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)  # پاسخ ادمین
    status = models.CharField(max_length=1, choices=TICKET_STATUS_CHOICES, default=TICKET_STATUS_OPEN)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"
