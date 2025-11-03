from django.urls import reverse
from .models import Post

def free_resources_url(request):
    base_url = reverse('post-list')  # e.g. /blog/
    try:
        has_free_resources = Post.objects.filter(is_free_resource=True).exists()
        if has_free_resources:
            url = f"{base_url}?free_resources=true"
    except Exception:
        url = base_url
    return {'free_resources_url': url}
