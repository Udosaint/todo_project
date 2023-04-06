import random
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


def send_verify_link(recipient_list, token):
    message = f'Your verification link is {token}'
    html = render_to_string('todo/emails/verify_email.html',{
        'token':token
    })
    send_mail("Verify Your Account", message, "noreply@tbnotes.com", [recipient_list], html_message=html)


def send_otp(email):
    otp = ''.join(random.choice('0123456789') for _ in range(6))
    message = f'Your OTP is {otp}'
    html = render_to_string('todo/emails/verify_account.html',{
        'otp':otp
    })
    send_mail("Verify Your Account", message, "noreply@ugnotes.com.ng", [email], html_message=html)
    return otp

def account_success(email, username):
    message = 'Your account has been successfully verified'
    html = render_to_string('todo/emails/account_success.html',{
        'username':username
    })
    send_mail("Account Verification", message, "noreply@ugnotes.com.ng", [email], html_message=html)

# for 
def password_success(email, username):
    message = 'Your password has been change'
    html = render_to_string('todo/emails/password_success.html',{
        'username':username
    })
    send_mail("Password Change", message, "noreply@ugnotes.com.ng", [email], html_message=html)

def forgot_password_success(email, username):
    message = 'Your password has been reset'
    html = render_to_string('todo/emails/forgot_password_success.html',{
        'username':username
    })
    send_mail("Password Reset", message, "noreply@ugnotes.com.ng", [email], html_message=html)


def forgot_password_otp(email):
    otp = ''.join(random.choice('0123456789') for _ in range(6))
    message = f'Your OTP is {otp}'
    html = render_to_string('todo/emails/forgot_password.html',{
        'otp':otp
    })
    send_mail("Forgot Password", message, "noreply@ugnotes.com.ng", [email], html_message=html)
    return otp


def send_welcome_mail(email, username):

    html = render_to_string('todo/emails/welcome_email.html',{
        'username':username
    })
    send_mail("Welcome", f'Welcome {username} ', "noreply@ugnote.com.ng", [email], html_message=html)