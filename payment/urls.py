from django.conf import settings
from django.urls import path

from . import views

app_name='payment'


urlpatterns = [
    path('process/', views.payment_process, name='payment_process'),
    path('callback/', views.payment_callback_view, name='payment_callback'),
]
