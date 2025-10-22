from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404,HttpResponseForbidden
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

import os

from .forms import ProfileForm
from orders.models import Order,OrderItem
from products.models import Video, VideoFile

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user)

        # ✅ Add all user orders (with their items and products)
        user = self.request.user
        context["orders"] = (
            Order.objects.filter(user=user, is_paid=True)
            .prefetch_related("items__product")
            .order_by("-datetime_created")
        )

        # Optional future stats
        # context["active_orders"] = context["orders"].filter(status="processing").count()
        # context["wallet_balance"] = user.wallet.balance if hasattr(user, "wallet") else 0

        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)

@login_required
def video_files_list(request, order_item_id):
    # پیدا کردن آیتم سفارش
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user, order__is_paid=True)

    # پیدا کردن ویدیوهای مربوط به محصول
    videos = Video.objects.filter(product=order_item.product)

    if not videos.exists():
        raise Http404("ویدیویی برای این محصول یافت نشد.")

    # فقط یکی از ویدیوها را تستی دانلود کنیم (یا می‌توانی لیست کامل بسازی)
    video = videos.first()
    file_path = video.video.path  # مسیر فیزیکی فایل (مثلاً /var/protected_videos/slug/1.mp4)

    if not os.path.exists(file_path):
        raise Http404("فایل یافت نشد.")

   
@login_required
def download_video_xaccel(request, file_id):
    vf = get_object_or_404(VideoFile, id=file_id)

    # چک مجوز دسترسی کاربر
    order_item = OrderItem.objects.filter(
        product=vf.video.product,
        order__user=request.user,
        order__is_paid=True
    ).first()
    if not order_item:
        return HttpResponseForbidden("دسترسی ندارید.")

    real_path = vf.file.path
    if not os.path.exists(real_path):
        raise Http404("فایل پیدا نشد.")

    internal_path = f"/protected_videos_internal/{vf.file.name}"

    response = HttpResponse()
    response["X-Accel-Redirect"] = internal_path
    response["Content-Disposition"] = f'attachment; filename="{os.path.basename(real_path)}"'
    return response