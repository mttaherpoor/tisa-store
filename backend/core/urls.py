from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.ProfileDetailView.as_view(), name="profile"),
    # path('download/<int:file_id>/', views.download_video_xaccel, name='download_video'),
    path("api/video/<int:file_id>/stream/", views.VideoDownloadURLView.as_view(),name='download-video'),
    path('videos/<int:order_item_id>/', views.VideoFilesListView.as_view(), name='video-file-list'),
]
