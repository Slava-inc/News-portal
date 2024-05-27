from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreate

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='product_create'),
    ]