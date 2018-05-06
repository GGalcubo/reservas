# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Provincia, Localidad, Calle, Estado, EstadoCivil, CategoriaCliente, CategoriaUnidad, TipoPersona, TipoObservacion, TipoLicencia, Adjunto, TipoTelefono, Telefono, Observacion, Licencia, Persona, Vehiculo, Unidad, Cliente, Viaje, ViajeHistorial, Trayecto, CentroCosto, PersonaCliente, ObservacionPersona, ObservacionUnidad, ObservacionVehiculo, ObservacionCliente, ObservacionViaje, ObservacionCentroCosto, ObservacionLicencia, TelefonoPersona, TelefonoCliente, AdjuntoViaje

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
    list_display = ('factura', 'proforma', 'estado', 'fecha', 'cliente', 'unidad', 'base_total')

admin.site.register(Viaje,ViajeAdmin)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Calle)
admin.site.register(Estado)
admin.site.register(EstadoCivil)
admin.site.register(CategoriaCliente)
admin.site.register(CategoriaUnidad)
admin.site.register(TipoObservacion)
admin.site.register(TipoLicencia)
admin.site.register(TipoTelefono)
admin.site.register(Adjunto)
admin.site.register(Telefono)
admin.site.register(Observacion)
admin.site.register(Licencia)
admin.site.register(Persona)
admin.site.register(Vehiculo)
admin.site.register(Unidad)
admin.site.register(Cliente)
admin.site.register(ViajeHistorial)
admin.site.register(Trayecto)
admin.site.register(CentroCosto)
admin.site.register(PersonaCliente)
admin.site.register(ObservacionPersona)
admin.site.register(ObservacionUnidad)
admin.site.register(ObservacionVehiculo)
admin.site.register(ObservacionCliente)
admin.site.register(ObservacionViaje)
admin.site.register(ObservacionCentroCosto)
admin.site.register(ObservacionLicencia)
admin.site.register(TelefonoPersona)
admin.site.register(TelefonoCliente)
admin.site.register(AdjuntoViaje)
admin.site.register(Permission)