from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('system/<int:pk>/edit/', views.edit_system, name='edit_system'),
    path('system/<int:system_id>/media-index/', views.system_media_index, name='system_media_index'),
]
