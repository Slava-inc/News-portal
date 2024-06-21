from celery import shared_task
import time

from news.signals import notify_about_new_post 

from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category
from django.conf import settings

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def send_news_notification(**kwargs):
    notify_about_new_post(None, kwargs['object'], action=kwargs['action'])
    # print([key for key in kwargs.keys()])


@shared_task
def my_job():
  # Your job processing logic here...
  start_day = datetime.datetime.today() - datetime.timedelta(days=7)
  qs = Post.objects.filter(time_in__gte=start_day).values('category')
  cat_id = list(set([r['category'] for r in qs]))

  subscribers_emails = {}
  for r in cat_id:
    if r == None:
      continue
    cat = Category.objects.get(id=r)
    subscribers_emails[cat.name] = []
    subscribers = cat.subscribers.all()
    subscribers_emails[cat.name] += [a.email for a in subscribers] # Добавление почт подписчиков
    send_email(cat, subscribers_emails[cat.name], start_day)    


def send_email(cat, subscriber_emails, start_day):
  posts = Post.objects.filter(time_in__gte=start_day, category=cat)

  html_content = render_to_string(
        'post_list.html',
        {
            'category_news_list': posts,
            'category': cat
        }
    )

  msg = EmailMultiAlternatives(
        subject=f'News in category {cat.name}', # Заголовок
        body='', # Тело пустое т.к. используем шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscriber_emails), # Кому отправляем
    )
    # Добавляем к сообщению наш шаблон
  msg.attach_alternative(html_content, 'text/html')
  msg.send()
  
