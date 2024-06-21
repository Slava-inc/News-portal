from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from email import message
from django.conf import settings
from .models import PostCategory, Category
from django.contrib.auth.models import User


# Отправка сообщений
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title, # Заголовок
        body='', # Тело пустое т.к. используем шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers), # Кому отправляем
    )
    # Добавляем к сообщению наш шаблон
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    # raise Exception('receiver called!')
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [a.email for a in subscribers] # Добавление почт подписчиков

        send_notifications(instance.preview(), instance.pk, instance.header, set(subscribers_emails))


def send_congratulations(user_name, email):
    html_content = render_to_string(
        'user_congratulation.html',
        {
            'text': f'Congratulations, {user_name}! You sing up on News portal.',
            'link': f'{settings.SITE_URL}/sign/login'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Congratulations from News portal', # Заголовок
        body='', # Тело пустое т.к. используем шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email], # Кому отправляем
    )
    # Добавляем к сообщению наш шаблон
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(post_save, sender=User)
def notify_new_author(sender, instance, **kwargs):
    if kwargs['created']:
        send_congratulations(instance.username, instance.email)
        # raise Exception('Hello, Signals!')