from django.urls import path, re_path as rp

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    rp(
        r"^(?P<slug>[-\w\u0600-\u06FF]+)/$",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    rp(
    r"comment/(?P<slug>[-\w\u0600-\u06FF]+)/$",
    views.CommentCreateView.as_view(),
    name="comment_create",
    ),
    # path("comment/<int:product_id>/", CommentCreateView.as_view(), name="comment_create"),
]
#urls.py
urlpatterns += [
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
