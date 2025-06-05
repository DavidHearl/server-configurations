from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('components/', views.components, name='components'),  # Added trailing slash
    path('components', views.components, name='components_no_slash'),  # Also match without slash
    
    # CPU routes
    path('components/add-cpu/', views.add_cpu, name='add_cpu'),
    path('components/edit-cpu/<int:cpu_id>/', views.edit_cpu, name='edit_cpu'),
    path('components/delete-cpu/<int:cpu_id>/', views.delete_cpu, name='delete_cpu'),
    
    # RAM routes
    path('components/add-ram/', views.add_ram, name='add_ram'),
    path('components/edit-ram/<int:ram_id>/', views.edit_ram, name='edit_ram'),
    path('components/delete-ram/<int:ram_id>/', views.delete_ram, name='delete_ram'),
    
    # Motherboard routes
    path('components/add-motherboard/', views.add_motherboard, name='add_motherboard'),
    path('components/edit-motherboard/<int:motherboard_id>/', views.edit_motherboard, name='edit_motherboard'),
    path('components/delete-motherboard/<int:motherboard_id>/', views.delete_motherboard, name='delete_motherboard'),
    
    # NIC routes
    path('components/add-nic/', views.add_nic, name='add_nic'),
    path('components/edit-nic/<int:nic_id>/', views.edit_nic, name='edit_nic'),
    path('components/delete-nic/<int:nic_id>/', views.delete_nic, name='delete_nic'),
    
    # PSU routes
    path('components/add-psu/', views.add_psu, name='add_psu'),
    path('components/edit-psu/<int:psu_id>/', views.edit_psu, name='edit_psu'),
    path('components/delete-psu/<int:psu_id>/', views.delete_psu, name='delete_psu'),
    
    # Case routes
    path('components/add-case/', views.add_case, name='add_case'),
    path('components/edit-case/<int:case_id>/', views.edit_case, name='edit_case'),
    path('components/delete-case/<int:case_id>/', views.delete_case, name='delete_case'),
    
    # Storage routes
    path('components/add-storage/', views.add_storage, name='add_storage'),
    path('components/edit-storage/<int:storage_id>/', views.edit_storage, name='edit_storage'),
    path('components/delete-storage/<int:storage_id>/', views.delete_storage, name='delete_storage'),
    
    # Rack routes
    path('components/add-rack/', views.add_rack, name='add_rack'),
    path('components/edit-rack/<int:rack_id>/', views.edit_rack, name='edit_rack'),
    path('components/delete-rack/<int:rack_id>/', views.delete_rack, name='delete_rack'),
    
    path('databases/', views.databases, name='databases'),  # Added trailing slash
    path('databases', views.databases, name='databases_no_slash'),  # Also match without slash
]