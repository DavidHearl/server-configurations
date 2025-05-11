from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-system/', views.add_system, name='add_system'),
    path('add-component/', views.add_component, name='add_component'),
]