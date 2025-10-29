from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.tasks import send_welcome_email_task

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    وقتی کاربر جدید ساخته شد، ایمیل HTML خوش‌آمدگویی با Celery ارسال شود
    """
    if created and instance.email:
        send_welcome_email_task.delay(instance.username, instance.email)
