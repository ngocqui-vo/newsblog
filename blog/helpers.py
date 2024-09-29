from django.core.mail import send_mail
from django.conf import settings


def send_contact(email, name,from_mail,website, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    subject = f'name: {name}, email: {from_mail}, website: {website}'
    send_mail(subject, message, email_from, recipient_list)
    return 1