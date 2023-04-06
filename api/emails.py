from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

import random


def send_verify_link(recipient_list, token):
    message = f'Your verification link is {token}'
    html = render_to_string('todo/emails/verify_email.html',{
        'token':token
    })
    send_mail("Verify Your Account", message, "noreply@tbnotes.com", [recipient_list], html_message=html)


# def send_otp(otp):
    
#     message = f'Your OTP is {otp}'
#     print(message)
    
    
def send_otp():
    otp = ''.join(random.choice('0123456789') for _ in range(6))
    message = f'Your OTP is {otp}'
    print(message)
    return otp