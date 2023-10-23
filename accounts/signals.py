from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from accounts.models import AuthorPost
from django.core.signals import request_started,got_request_exception,request_finished
from django.dispatch import receiver

@receiver(post_save, sender=AuthorPost)
def reset_password_mail(sender, instance, **kwargs):
    if instance.author:
        user_email = instance.author.email
        mail_subject = 'Post is created.'
        message = render_to_string('post_created_mail.html')
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, "", from_email, [user_email], fail_silently=True, html_message=message)
