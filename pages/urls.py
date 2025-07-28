from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("aboutus/", views.AboutUsPageView.as_view(), name="aboutus"),
    path(
        "free_resources/", views.FreeResourcesPageView.as_view(), name="free_resources"
    ),
    path("startup/", views.StartupPageView.as_view(), name="startup"),
    path("contactus/", views.ContactUsPageView.as_view(), name="contactus"),
    path("contactus/", views.ContactUsPageView.as_view(), name="contactus"),
]
