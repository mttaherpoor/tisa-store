from django.contrib import admin

from .models import Post, Category, Comment
from .forms import PostForm


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = [
        "author",
        "body",
        "stars",
        "active",
    ]
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ("title", "author", "status", "datetime_created","category","slug")
    ordering = ("status",)
    prepopulated_fields = {"slug": ("title",)}
    # readonly_fields = [
    #     "slug",
    # ]

    def save_model(self, request, obj, form, change):
        if not change:  # پست جدید
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # وقتی پست در حال ویرایش است
            return self.readonly_fields + ("author",)
        return self.readonly_fields

    inlines = [
        CommentsInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "author",
        "body",
        "stars",
        "active",
    ]
