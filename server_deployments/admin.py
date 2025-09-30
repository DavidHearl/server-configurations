from django.contrib import admin
from .models import *

admin.site.register(CPU)
admin.site.register(RAM)
admin.site.register(Motherboard)
admin.site.register(NIC)
admin.site.register(PSU)
admin.site.register(Case)
admin.site.register(Rack)
admin.site.register(System)
admin.site.register(StorageDevice)
# admin.site.register(IndexedFile)
# admin.site.register(IndexedFolder)