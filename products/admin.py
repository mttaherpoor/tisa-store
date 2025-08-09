from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from django import forms

from .models import Category, Product, Comment
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
