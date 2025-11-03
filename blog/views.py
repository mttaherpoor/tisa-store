from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy 
from django.utils.translation import gettext as _
from django.views import generic

from .forms import CategoryForm, PostForm , CommentForm 
from .models import Category, Post, Comment


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "post_list"
    paginate_by = 9


    # def get_queryset(self):
    #     return Post.objects.filter(status="pub").order_by(
    #         "-datetime_modified"
    #     )  # - desc
    
    def get_queryset(self):
        queryset = Post.objects.filter(status="pub").order_by("-datetime_modified")
        category_name = self.request.GET.get("category")  # <-- from URL query (?category=)

        if category_name:
            queryset = queryset.filter(category__name=category_name)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = Comment.objects.filter(post=self.object, active=True)
        return context



class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = PostForm
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # 👈 نویسنده = کاربر فعلی
        return super().form_valid(form)

    # فقط ادمین‌ها اجازه ایجاد پست داشته باشن
    def test_func(self):
        return self.request.user.is_staff


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"

    def test_func(self):
        post = self.get_object()
        # فقط نویسنده یا ادمین بتواند ویرایش کند
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        # فقط نویسنده یا ادمین بتواند حذف کند
        return self.request.user == post.author or self.request.user.is_staff
    

# class CommentCreateView(generic.CreateView):
#     model = Comment
#     form_class = CommentForm

#     # def get_success_url(self):
#     #     return reverse('product_list')

#     def form_valid1(self, form):
#         obj = form.save(commit=False)
#         obj.author = self.request.user

#         post_slug = self.kwargs["slug"]
#         post = get_object_or_404(Post, slug=post_slug)
#         obj.post = post
#         # obj.save()

#         # return redirect(post.get_absolute_url()) 
#         return super().form_valid(form)
    
    
#     def form_valid(self, form):
#         post = get_object_or_404(Post, slug=self.kwargs["slug"])
#         comment = form.save(commit=False)
#         comment.author = self.request.user
#         comment.post = post
#         comment.save()
#         messages.success(self.request, _("Comment successfully created"))
#         return redirect(post.get_absolute_url())
#         messages.success(self.request, "کامنت شما ثبت شد و پس از تأیید نمایش داده می‌شود.")


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('product_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        post_slug = self.kwargs["slug"]
        post = get_object_or_404(Post, slug=post_slug)
        obj.post = post

        messages.success(self.request, _("Comment successfully created"))

        return super().form_valid(form)

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = CategoryForm
    template_name = "blog/category_create.html"
    success_url = reverse_lazy("post-create")
    
    # def form_valid(self, form):
    #     form.save()  # 👈 خودمون ذخیره می‌کنیم response = super().form_valid(form)
    #     return redirect(self.request.META.get('HTTP_REFERER', '/'))

    # فقط ادمین‌ها اجازه ایجاد پست داشته باشن
    def test_func(self):
        return self.request.user.is_staff