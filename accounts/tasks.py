from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_welcome_email_task(username, email):
    """
    ارسال ایمیل HTML خوش‌آمدگویی با قالب Template
    """
    subject = "🌷 خوش آمدید به سایت ما!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        "username": username,
        "domain": "yourdomain.com",  # یا از settings.SITE_DOMAIN بخوان
        "site_name": "Tisa Store"
    }

    html_content = render_to_string("emails/welcome_email.html", context)
    text_content = f"سلام {username}!\nبه Tisa Store خوش آمدید 🌸"

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        print(f"✅ ایمیل HTML خوش‌آمدگویی برای {email} ارسال شد.")
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل به {email}: {e}")
