from django.urls import path, include
from . import views
from .views import hello_view

urlpatterns = [
    path('', views.main),
    path('hello/', hello_view, name='hello'),
]