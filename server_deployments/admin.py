from django.contrib import admin
from .models import *


class DjangoStepInline(admin.TabularInline):
    model = DjangoStep
    extra = 1
    fields = ['order', 'title', 'step_type', 'content']


@admin.register(DjangoGuide)
class DjangoGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'updated_at']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [DjangoStepInline]


@admin.register(DjangoStep)
class DjangoStepAdmin(admin.ModelAdmin):
    list_display = ['title', 'guide', 'order', 'step_type', 'updated_at']
    list_filter = ['guide', 'step_type']
    list_editable = ['order']
    search_fields = ['title', 'content']


admin.site.register(CPU)
admin.site.register(RAM)
admin.site.register(Motherboard)
admin.site.register(NIC)
admin.site.register(PSU)
admin.site.register(Case)
admin.site.register(Rack)
admin.site.register(System)
admin.site.register(StorageDevice)


@admin.register(DashboardLink)
class DashboardLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'category', 'tab', 'order', 'active', 'updated_at']
    list_filter = ['tab', 'category', 'active']
    list_editable = ['order', 'active']
    search_fields = ['name', 'url', 'description']
    ordering = ['tab', 'category', 'order', 'name']


# admin.site.register(IndexedFile)
# admin.site.register(IndexedFolder)