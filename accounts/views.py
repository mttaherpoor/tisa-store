from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, Http404,HttpResponseForbidden
from django.shortcuts import get_object_or_404,render
from django.views.generic import TemplateView

import os

from .forms import ProfileForm
from orders.models import Order,OrderItem
from products.models import Video, VideoFile

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user)

        context["password_form"] = PasswordChangeForm(user=self.request.user)
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
        if "new_password1" in request.POST:
            # 🔹 Handle password change
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevent logout
                messages.success(request, "رمز عبور شما با موفقیت تغییر یافت.")
            else:
                messages.error(request, "خطا در تغییر رمز عبور. لطفاً مجدداً تلاش کنید.")
            return self.get(request, *args, **kwargs)
        
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد.")
        return self.get(request, *args, **kwargs)


@login_required
def video_files_list(request, order_item_id):
    try:
        order_item = OrderItem.objects.get(
            id=order_item_id,
            order__user=request.user,
            order__is_paid=True
        )
    except OrderItem.DoesNotExist:
        return HttpResponseForbidden("دسترسی ندارید.")

    # پیدا کردن ویدیوهای محصول خریداری‌شده
    videos = Video.objects.filter(product=order_item.product).prefetch_related("files")

    if not videos.exists():
        raise Http404("ویدیویی برای این محصول یافت نشد.")

    # پیدا کردن فایل‌های تمام ویدیوها
    video_files = VideoFile.objects.filter(video__in=videos)

    if not video_files.exists():
        raise Http404("فایلی برای این ویدیو یافت نشد.")
    
    # بازگرداندن به قالب
    return render(
        request,
        "accounts/video_files_list.html",
        {
            "product": order_item.product,
            "video_files": video_files,
        }
    )

   
@login_required
def download_video_xaccel(request, file_id):
    vf = get_object_or_404(VideoFile, id=file_id)

    # ✅ بررسی اینکه کاربر واقعاً محصول را خریده باشد
    has_access = OrderItem.objects.filter(
        product=vf.video.product,
        order__user=request.user,
        order__is_paid=True
    ).exists()

    if not has_access:
        return HttpResponseForbidden("دسترسی ندارید.")

    real_path = vf.file.path
    if not os.path.exists(real_path):
        raise Http404("فایل پیدا نشد.")

    # ✅ مسیر داخلی برای Nginx
    internal_path = f"/protected_videos_internal/{vf.file.name}"

    response = HttpResponse()
    response["X-Accel-Redirect"] = internal_path
    response["Content-Disposition"] = f'attachment; filename="{os.path.basename(real_path)}"'
    response["Content-Type"] = "application/octet-stream"
    return response