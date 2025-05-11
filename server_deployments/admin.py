from django.contrib import admin
from .models import Rack, System, Component

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'size')
    search_fields = ('name',)

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'rack', 'size')
    list_filter = ('rack',)
    search_fields = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('component_type', 'model', 'unit_price')
    list_filter = ('component_type',)
    search_fields = ('model',)
