from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)

class CategoryAdmin(TranslationAdmin):
    model = Category
 
 
class PostAdmin(TranslationAdmin):
    model = Post

admin.site.register(Post)
admin.site.register(Category)