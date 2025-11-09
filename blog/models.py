from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django_ckeditor_5.fields import CKEditor5Field
import os

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (("pub", "Published"), ("drf", "Draft"))

    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts",blank=True)
    slug = models.SlugField()
    text = CKEditor5Field(_("Post description"), config_name="extends")
    # auther = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)
    pdf = models.FileField(upload_to='blog/pdfs/', blank=True, null=True)
    is_free_resource  =models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def pdf_filename(self):
        if self.pdf:
            return os.path.basename(self.pdf.name)
        return ""

class ActiveCommentsManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    POST_STARS = [
        ("1", _("Very Bad")),
        ("2", _("Bad")),
        ("3", _("Normal")),
        ("4", _("Good")),
        ("5", _("Perfect")),
    ]

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments",)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="post_comments",verbose_name="Comment author",)
    body = models.TextField(verbose_name=_("Comment Text"))
    stars = models.CharField(max_length=10, choices=POST_STARS, verbose_name=_("What is your score?"))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    # Manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManger()

    def get_absolute_url(self):
        return self.post.get_absolute_url()
        return reverse("post_detail", args=[self.post.id])
