from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .models import FAQ
from .forms import ContactForm 
from products.models import Product
from  blog.models import Post


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()[:3]
        posts = Post.objects.all()[:3]
        faqs = FAQ.objects.all()
        context = super().get_context_data(**kwargs)
        context["products"] = products
        context["posts"] = posts
        context["faqs"] =faqs
        return context

class AboutUsPageView(TemplateView):
    template_name = "pages/aboutus.html"


class ContactUsPageView(FormView):
    template_name = "pages/contactus.html"
    form_class = ContactForm
    success_url = reverse_lazy('contactus')  # redirect after success

    def form_valid(self, form):
        # Process the form (save, send email, etc.)
        form.save()  # or custom logic
        messages.success(self.request, "Your message has been sent successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_url'] = reverse_lazy('account_signup')  # example
        return context


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
