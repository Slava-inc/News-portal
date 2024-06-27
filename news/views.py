from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category
from django.urls import reverse_lazy
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from board.tasks import send_news_notification

from django.utils.translation import gettext as _ # импортируем функцию для перевода

import logging

from rest_framework import viewsets
from rest_framework import permissions

from news.serializers import *

logger = logging.getLogger(__name__)

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['length'] = None

        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset   
        return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     send_news_notification(object=context['object'], action='post_add')
    #     return context
    

class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'header'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 5

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs  
    
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['length'] = None

        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset   
        return context  
    
class PostCreate(PermissionRequiredMixin, CreateView):
    
    permission_required = ('news.add_post', )
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NE' if self.request.path[:5] == '/news' else 'AR' 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        send_news_notification(object=self.object, action='post_add')
        return context    

# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _('You subscribed on category')

    return render(request, 'subscribe.html', {'category': category, 'message': message})


# rest views
# class SchoolViewset(viewsets.ModelViewSet):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer

import json


def news(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps([
            {
                "header":post.header,
                "author":post.author,
                "category":post.category
            } for post in Post.objects.all()
        ]))
    if request.method == 'POST':
        # Нужно извлечь параметы из тела запроса
        json_params = json.loads(request.body)

        post = Post.objects.create(
            header=json_params['header'],
            category=json_params['category']
        )
        return HttpResponse(json.dumps({
            "header":post.header,
            "category":post.category,
        }))


def post_id(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        return HttpResponse(json.dumps(
             {
                "id":post.id,
                "author":post.author,
                "header":post.header,
                "category":post.category
            }))
    json_params = json.loads(request.body)
    if request.method == 'PUT':
        post.header = json_params['header']
        post.category = json_params['category']
        post.save()
        return HttpResponse(json.dumps({
            "id":post.id,
            "header":post.header,
            "category":post.category
        }))

