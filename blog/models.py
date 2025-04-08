from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    STATUS_CHOICES = (("pub", "Published"), ("drf", "Draft"))

    title = models.CharField(max_length=100)
    text = CKEditor5Field(_("Product description"), config_name="extends")
    auther = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    auther = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.id])
