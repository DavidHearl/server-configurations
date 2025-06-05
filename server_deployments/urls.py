from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('components', views.components, name='components'),
    path('databases', views.databases, name='databases'),
]
