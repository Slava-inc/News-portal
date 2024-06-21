from django.urls import path
from .views import IndexView

urlpatterns = [
    path('task/', IndexView.as_view()),
]