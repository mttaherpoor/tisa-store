from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views import View
from django.views.generic import TemplateView

import boto3

import os
from datetime import timedelta

from products.models import Video, VideoFile
from orders.models import Order,OrderItem

from .forms import ProfileForm,TicketForm
from .models import Ticket

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "core/profile.html"

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


class VideoDownloadURLView(LoginRequiredMixin, View):

    def get(self, request, file_id):
        video_file = get_object_or_404(
            VideoFile.objects.select_related("video__product").filter(
                id=file_id,
                video__product__orderitem__order__user=request.user,
                video__product__orderitem__order__is_paid=True,
            )
        )

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
                "Key": video_file.file.name,
                "ResponseContentDisposition": (
                    f'attachment; filename="{video_file.filename or video_file.file.name}"'
                ),
            },
            ExpiresIn=600,
        )

        return JsonResponse({"download_url": url})


class VideoFilesListView(LoginRequiredMixin, View):
    template_name = "core/video_files_list.html"

    def get(self, request, order_item_id):
        order_item = get_object_or_404(
            OrderItem,
            id=order_item_id,
            order__user=request.user,
            order__is_paid=True,
        )

        videos = Video.objects.filter(product=order_item.product).prefetch_related("files")

        if not videos.exists():
            raise Http404("ویدیویی برای این محصول یافت نشد.")

        video_files = VideoFile.objects.filter(video__in=videos)

        if not video_files.exists():
            raise Http404("فایلی برای این ویدیو یافت نشد.")

        return render(request,self.template_name,{
                "product": order_item.product,
                "video_files": video_files,
            },
        )
