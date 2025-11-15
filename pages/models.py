from django.db import models

class FAQ(models.Model):
    question = models.CharField("سؤال", max_length=255)
    answer = models.TextField("پاسخ")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "سؤال متداول"
        verbose_name_plural = "سؤالات متداول"

    def __str__(self):
        return self.question
