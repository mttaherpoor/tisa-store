from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget#,CKEditor5UploadingWidget

from .models import Category, Comment, Post

from django.utils.text import slugify

class PostForm(forms.ModelForm):
    slug = forms.CharField(
        required=False,
        label="Slug",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
    )

    class Meta:
        model = Post
        fields = ["title", "slug", "category", "text", "status","pdf"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post title"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            # "text": CKEditor5UploadingWidget(config_name="extends"),
            "text": CKEditor5Widget(config_name="extends"),
            #   forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Write your post content"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If instance exists, pre-fill slug
        if self.instance and self.instance.pk:
            self.fields["slug"].initial = self.instance.slug

    def clean_slug(self):
        """Ensure slug always matches the title."""
        title = self.cleaned_data.get("title", "")
        return slugify(title)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body",
            "stars",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']