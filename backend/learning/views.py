from django.views.generic import DetailView, ListView

from .models import LearningPath


class ActiveLearningPathMixin:
    """Limit public views to active learning paths."""

    def get_queryset(self):
        return (LearningPath.objects.filter(is_active=True).order_by("order", "title"))


class LearningPathListView(ActiveLearningPathMixin, ListView):
    model = LearningPath
    template_name = "learning/learning_path_list.html"
    context_object_name = "learning_paths"
    paginate_by = 12


class LearningPathDetailView(ActiveLearningPathMixin, DetailView):
    model = LearningPath
    template_name = "learning/learning_path_detail.html"
    context_object_name = "learning_path"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (super().get_queryset().prefetch_related("steps__course"))
