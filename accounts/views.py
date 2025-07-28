from django.views import generic

from .models import CustomUser


class ProfileDetailView(generic.DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "user"
