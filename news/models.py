from django.db import models
from django.contrib.auth.models import User
from news.resources import CATEGORIES, news
from django.urls import reverse
import datetime


class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts = Post.objects.filter(author=self)
        author_comments = Comment.objects.filter(user=self.user)
        rating = 0.0
        for p in posts:
            p_с = Comment.objects.filter(post=p) # post comments
            rating += sum([r.rating for r in p_с]) # post comment rating sum
        self.rating = sum([3 * r.rating for r in posts]) + sum([r.rating for r in author_comments]) + rating
        self.save()

    def __str__(self):
        return self.user.username 




class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser', related_name='subscribers')

    def __str__(self) -> str: 
        return self.name


class CategoryUser(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    

class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=CATEGORIES, default=news,)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharField(max_length=250, blank=False)
    text = models.CharField(blank=False, max_length=10000)
    rating = models.FloatField(default=0.0)
    
    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'
    

    def __str__(self):
        return f'{self.header.title()}: {self.preview()}'    

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    def author_today_posts(self):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min).date()
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max).date()

        return len(Post.objects.filter(author=self.author and self.time_in.replace(tzinfo=None).date()>=today_min and self.time_in.replace(tzinfo=None).date() <= today_max))


class PostCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(blank=False, max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


