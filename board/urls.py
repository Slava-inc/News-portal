from django.urls import path
from .views import IndexView

urlpatterns = [
    path('accounts/login/', IndexView.as_view()),
]