from django.shortcuts import render

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutUsPageView(TemplateView):
    template_name = "pages/aboutus.html"


class FreeResourcesPageView(TemplateView):
    template_name = "pages/free_resources.html"


class StartupPageView(TemplateView):
    template_name = "pages/aboutus.html"


class ContactUsPageView(TemplateView):
    template_name = "pages/contactus.html"


from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

def send_email(request):
    subject = 'موضوع ایمیل'
    message = 'این یک پیام آزمایشی است.'
    from_email = 'tisavista@gmail.com'
    recipient_list = ['mttaherpoor@gmail.com']  # آدرس ایمیل گیرنده

    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse("ایمیل ارسال شد!")