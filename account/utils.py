from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{ activation_code }'
    message = f"""
    Please activate your account.
    That you can use our Helpers-help.
    Activate: {activation_url}
    """
    send_mail(
        'Activate your account',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )

@shared_task
def send_reset_activation_code(user):
    activation_url = f'{user.activation_code}'
    message = f"""Restore password use code: {activation_url}"""
    to_email = user.email
    send_mail(
        'Activate your account',
        message,
        'test@test.com',
        [to_email],
        fail_silently=False,
    )