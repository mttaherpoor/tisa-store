from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    slug = models.SlugField()
    description = CKEditor5Field(_("Product description"), config_name="extends")
    short_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(blank=True)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(_("Product Image"),upload_to="product/product_cover/",blank=True)
    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ActiveCommentsManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ("1", _("Very Bad")),
        ("2", _("Bad")),
        ("3", _("Normal")),
        ("4", _("Good")),
        ("5", _("Perfect")),
    ]

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="comments",)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="product_comments",verbose_name="Comment author",)
    body = models.TextField(verbose_name=_("Comment Text"))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_("What is your score?"))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    # Manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManger()

    def get_absolute_url(self):
        return self.product.get_absolute_url()
        return reverse("product_detail", args=[self.product.get_absolute_url()])


def video_upload_path(instance, filename):
    return f"{instance.video.product.slug}/{instance.video.id}/{filename}"


class Video(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="videos"
    )
    title = models.CharField(max_length=255, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Video {self.id}"


class VideoFile(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=video_upload_path, storage=settings.PROTECTED_VIDEO_STORAGE)
    filename = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.filename or self.file.name