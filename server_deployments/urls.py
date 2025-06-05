from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('components/', views.components, name='components'),  # Added trailing slash
    path('components', views.components, name='components_no_slash'),  # Also match without slash
    path('components/add-cpu/', views.add_cpu, name='add_cpu'),
    path('components/edit-cpu/<int:cpu_id>/', views.edit_cpu, name='edit_cpu'),
    path('components/delete-cpu/<int:cpu_id>/', views.delete_cpu, name='delete_cpu'),
    path('databases/', views.databases, name='databases'),  # Added trailing slash
    path('databases', views.databases, name='databases_no_slash'),  # Also match without slash
]
