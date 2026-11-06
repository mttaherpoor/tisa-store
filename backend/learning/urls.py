from django.urls import path

from .views import LearningPathDetailView, LearningPathListView

urlpatterns = [
    path("", LearningPathListView.as_view(), name="learning_path_list"),
    path("<slug:slug>/", LearningPathDetailView.as_view(), name="learning_path_detail"),
]
