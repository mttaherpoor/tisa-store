from django.urls import reverse
from .models import Category

def free_resources_url(request):
    try:
        category = Category.objects.get(name="free resources")
        # use query parameter instead of path
        base_url = reverse('post-list')  # e.g. /blog/
        url = f"{base_url}?category={category.name}"
    except Category.DoesNotExist:
        url = reverse('post-list')  # fallback to all posts
    return {'free_resources_url': url}
