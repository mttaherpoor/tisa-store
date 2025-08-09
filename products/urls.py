from django.urls import path
from django.urls import re_path

from .views import ProductListView, ProductDetailView, CommentCreateView

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    re_path(
        r"^(?P<slug>[-\w\u0600-\u06FF]+)/$",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "comment/<int:product_id>/", CommentCreateView.as_view(), name="comment_create"
    ),
]
