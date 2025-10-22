from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from django import forms

from .models import Category, Product, Comment,Video,VideoFile
from .forms import ProductForm


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = [
        "author",
        "body",
        "stars",
        "active",
    ]
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    form = ProductForm
    list_display = [
        "title",
        "price",
        "active",
        "slug",
    ]

    inlines = [
        CommentsInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    # readonly_fields = ("slug",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "author",
        "body",
        "stars",
        "active",
    ]


@admin.register(Category)
class CategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "title",
        "top_product",
    ]


class VideoFileInline(admin.TabularInline):  # یا StackedInline اگر بخواهی ظاهر عمودی‌تر
    model = VideoFile
    extra = 1  # تعداد فرم‌های خالی پیش‌فرض برای افزودن فایل جدید
    fields = ['file', 'filename']
    verbose_name = "فایل ویدیو"
    verbose_name_plural = "فایل‌های ویدیو"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'datetime_created', 'datetime_modified']
    list_filter = ['product']
    search_fields = ['title', 'product__title']
    inlines = [VideoFileInline]


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ['video', 'filename', 'file']
    search_fields = ['filename', 'video__title']