from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views.generic import TemplateView


import boto3
import os
from datetime import timedelta

from .forms import ProfileForm,TicketForm
from orders.models import Order,OrderItem
from products.models import Video, VideoFile
from .models import Ticket

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        # فرم‌ها
        context["form"] = ProfileForm(instance=user)
        context["ticket_form"] = TicketForm()
        context["password_form"] = PasswordChangeForm(user=user)

        # سفارش‌ها با prefetch برای آیتم‌ها و محصولاتشان
        context["orders"] = (
            Order.objects.filter(user=user, is_paid=True)
            .prefetch_related("items__product")  # prefetch همه آیتم‌ها و محصولاتشان
            .order_by("-datetime_created")
        )

        # تیکت‌ها با select_related برای کاربر
        context["tickets"] = Ticket.objects.filter(user=user).select_related("user").order_by("-datetime_created")

        return context

    def post(self, request, *args, **kwargs):

        # 1️⃣ تغییر رمز عبور
        if "new_password1" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "رمز عبور شما با موفقیت تغییر یافت.")
            else:
                messages.error(request, "خطا در تغییر رمز عبور.")
            return self.get(request, *args, **kwargs)

        # 2️⃣ ارسال تیکت
        if "subject" in request.POST:
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                messages.success(request, "تیکت شما با موفقیت ثبت شد. پشتیبانی به زودی پاسخ می‌دهد.")
            else:
                messages.error(request, "خطایی رخ داد. لطفاً فرم تیکت را بررسی کنید.")
            return self.get(request, *args, **kwargs)

        # 3️⃣ فرم پروفایل
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد.")
        else:
            messages.error(request, "خطا! اطلاعات پروفایل معتبر نیست.")

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

   
# @login_required
# def download_video_xaccel(request, file_id):
#     vf = get_object_or_404(VideoFile, id=file_id)

#     # ✅ بررسی اینکه کاربر واقعاً محصول را خریده باشد
#     has_access = OrderItem.objects.filter(
#         product=vf.video.product,
#         order__user=request.user,
#         order__is_paid=True
#     ).exists()

#     if not has_access:
#         return HttpResponseForbidden("دسترسی ندارید.")

#     real_path = vf.file.path
#     if not os.path.exists(real_path):
#         raise Http404("فایل پیدا نشد.")

#     # ✅ مسیر داخلی برای Nginx
#     internal_path = f"/protected_videos_internal/{vf.file.name}"    
#     response = HttpResponse()
#     response["X-Accel-Redirect"] = internal_path
#     response["Content-Disposition"] = f'attachment; filename="{os.path.basename(real_path)}"'
#     response["Content-Type"] = "application/octet-stream"
#     return response

# @login_required
# def get_video_stream_url(request, file_id):

#     vf = VideoFile.objects.get(id=file_id)

#     # 🔐 access check
#     has_access = vf.video.product.orderitem_set.filter(
#         order__user=request.user,
#         order__is_paid=True
#     ).exists()

#     if not has_access:
#         return HttpResponseForbidden("No access")

#     s3 = boto3.client(
#         "s3",
#         endpoint_url=settings.AWS_S3_ENDPOINT_URL,
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         region_name=settings.AWS_S3_REGION_NAME,
#     )

#     url = s3.generate_presigned_url(
#         ClientMethod="get_object",
#         Params={
#             "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
#             "Key": vf.file.name,
#             "ResponseContentType": "video/mp4",
#             "ResponseContentDisposition": "inline",
#         },
#         ExpiresIn=1200,  # 10 minutes
#     )

#     return JsonResponse({
#         "stream_url": url
#     })

@login_required
def get_video_download_url(request, file_id):
    vf = VideoFile.objects.get(id=file_id)

    # 🔐 access check (same logic you already use)
    has_access = vf.video.product.orderitem_set.filter(
        order__user=request.user,
        order__is_paid=True
    ).exists()

    if not has_access:
        return HttpResponseForbidden("No access")

    s3 = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": vf.file.name,
            "ResponseContentDisposition": f'attachment; filename="{vf.filename or vf.file.name}"'
        },
        ExpiresIn=600,  # 10 min valid
    )

    return JsonResponse({
        "download_url": url
    })
