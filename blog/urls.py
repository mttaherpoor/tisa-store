from django.urls import path, re_path as rp

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    
    path('posts/category/<str:category_name>/', views.PostListView.as_view(), name='post-list-by-category'),
    # path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path('add-category/', views.CategoryCreateView.as_view(), name='category-create'),
    rp(r"^(?P<slug>[-\w\u0600-\u06FF]+)/$",views.PostDetailView.as_view(),name="post_detail"),
    rp(r"comment/(?P<slug>[-\w\u0600-\u06FF]+)/$",views.CommentCreateView.as_view(),name="blog-comment-create"),
]
