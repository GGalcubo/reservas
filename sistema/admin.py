# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Viaje, Estado

# Register your models here.
class EstadoAdmin(admin.ModelAdmin):
    
    list_display = ('estado',)
    fieldsets = (
        ('Principal', {
            'fields': ['estado']
        }),
    )

class ViajeAdmin(admin.ModelAdmin):
    
    list_display = ('factura', 'proforma', 'estado', 'fecha', 'hora', 'base_total', 'peaje_total', 'estacionamiento_total', 'maletas', 'bilingue')
    fieldsets = (
        ('Principal', {
            'fields': ['factura', 'proforma', 'estado', 'fecha', 'hora', 'base_total', 'peaje_total', 'estacionamiento_total', 'maletas', 'bilingue']
        }),
    )

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Viaje, ViajeAdmin)
admin.site.register(Permission)