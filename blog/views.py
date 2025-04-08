from django.views import generic
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(status="pub").order_by(
            "-datetime_modified"
        )  # - desc


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = "blog/post_create.html"


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("posts_list")
