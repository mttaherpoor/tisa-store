from django.views import generic
from django.shortcuts import get_object_or_404, reverse, render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages


from .models import Product, Comment, Category
from .forms import CommentForm


class ProductListView(generic.ListView):
    # model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_title = self.request.GET.get("category")

        if category_title:
            queryset = queryset.select_related('category').filter(category__title=category_title)

        return queryset

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('product_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_slug = self.kwargs["slug"]
        product = get_object_or_404(Product, slug=product_slug)
        obj.product = product

        messages.success(self.request, _("Comment successfully created"))

        return super().form_valid(form)
