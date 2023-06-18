from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, message, sender_mail, reciever_mail):
    send_mail(subject,
              message, sender_mail, [reciever_mail])
    
    return 'mail sent'
