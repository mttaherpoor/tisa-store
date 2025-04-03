from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect,reverse

import requests
import json

from orders.models import Order


methods = ['sandbox', 'payment']

def payment_process(request:HttpRequest):
    
    method = methods[0] if settings.DEBUG else methods[1]
    
    # Get order id from session
    order_id = request.session.get('order_id')
    
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = f"https://{method}.zarinpal.com/pg/v4/payment/request.json"

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data ={
        'merchant_id':settings.ZARINPAL_MERCHANT_ID,
        'amount':rial_total_price,
        'description':f'#{order.id}:{order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback'))
        
    }
     
    
    res = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    output = res.json()
    authority = output['data']['authority']
    order.zarinpal_authority = authority
    
    order.save()
#'errors' in output or
    if  len(output['errors']):
        return HttpResponse('Error from zarinpal')
    else :
        return redirect(f'https://{method}.zarinpal.com/pg/StartPay/{authority}')
    
def payment_callback_view(request:HttpRequest):
    
    method = methods[0] if settings.DEBUG else methods[1]

    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
        "accept": "application/json",
        "content-type": "application/json",
        }

        request_data ={
            'merchant_id':settings.ZARINPAL_MERCHANT_ID,
            'amount':rial_total_price,
            'authority':payment_authority,
        }

        res = requests.post(
            url=f'https://{method}.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )

        if  'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors'] == 0)):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')
            
            elif payment_code == 101:
                return HttpResponse(' پرداخت شما با موفقیت انجام شد.البته این تراکنش قبلا ثبت شده است.')

            else:
                error_code = res.json()['errors']['code']
                error_message =res.json()['errors']['message']
                return HttpResponse(f'{error_code}{error_message} تراکتش ناموفق بود.')
    else:
        return HttpResponse(' تراکتش ناموفق بود!.')
