from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Comment, Product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body",
            "stars",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="extends"),
        }
