from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('system/<int:pk>/edit/', views.edit_system, name='edit_system'),
]
