# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Viaje, Estado, CategoriaEmpresa, CategoriaVehiculo, TipoPersona, TipoObservacion, TipoLicencia, TipoTelefono, Telefono, Observacion, Licencia, Persona, Vehiculo, Empresa, PersonaEmpresa, ObservacionVehiculo, ObservacionEmpresa, ObservacionViaje, TelefonoPersona, TelefonoEmpresa, Adjunto, AdjuntoViaje, Trayecto, CentroCosto, Proveedor, ObservacionCentroCosto

class TrayectoInline(admin.TabularInline):
    model = Trayecto
    extra = 1

class ObservacionViajeInline(admin.TabularInline):
    model = ObservacionViaje
    extra = 1

class AdjuntoViajeInline(admin.TabularInline):
    model = AdjuntoViaje
    extra = 1

class ViajeAdmin(admin.ModelAdmin):
    inlines = [
        TrayectoInline, ObservacionViajeInline, AdjuntoViajeInline,
    ]
    list_display = ('factura', 'proforma', 'estado', 'fecha', 'empresa', 'proveedor', 'base_total')

admin.site.register(Viaje,ViajeAdmin)
admin.site.register(TipoTelefono)
admin.site.register(TipoLicencia)
admin.site.register(TipoObservacion)
admin.site.register(TipoPersona)
admin.site.register(CategoriaVehiculo)
admin.site.register(CategoriaEmpresa)
admin.site.register(Proveedor)
admin.site.register(CentroCosto)
admin.site.register(Estado)
admin.site.register(Observacion)
admin.site.register(Licencia)
admin.site.register(Persona)
admin.site.register(Vehiculo)
admin.site.register(Empresa)
admin.site.register(Adjunto)
admin.site.register(Trayecto)
admin.site.register(AdjuntoViaje)
admin.site.register(PersonaEmpresa)
admin.site.register(ObservacionVehiculo)
admin.site.register(ObservacionEmpresa)
admin.site.register(ObservacionViaje)
admin.site.register(ObservacionCentroCosto)
admin.site.register(TelefonoPersona)
admin.site.register(TelefonoEmpresa)
admin.site.register(Permission)