from django.urls import reverse
from .models import Post

def free_resources_url(request):
    base_url = reverse('post-list')

    if Post.objects.filter(is_free_resource=True).exists():
        return {'free_resources_url': f"{base_url}?free_resources=true"}

    return {'free_resources_url': base_url}
