# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Provincia, Localidad, Calle, Estado, EstadoCivil, CategoriaCliente, CategoriaViaje, TipoPersona, TipoObservacion, TipoLicencia, Adjunto, TipoTelefono, Telefono, Observacion, Licencia, Persona, Vehiculo, Unidad, Cliente, Viaje, ViajeHistorial, Trayecto, CentroCosto, PersonaCliente, ObservacionPersona, ObservacionUnidad, ObservacionVehiculo, ObservacionCliente, ObservacionViaje, ObservacionCentroCosto, ObservacionLicencia, TelefonoPersona, TelefonoCliente, AdjuntoViaje, Tarifario, MailCliente, MailPersona, LicenciaPersona, LicenciaVehiculo, ViajePasajero

class TrayectoInline(admin.TabularInline):
    model = Trayecto
    extra = 1

class PersonaClienteInline(admin.TabularInline):
    model = PersonaCliente
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

class ClienteAdmin(admin.ModelAdmin):
    inlines = [
        PersonaClienteInline,
    ]
    list_display = ('razon_social',)

admin.site.register(Viaje,ViajeAdmin)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Calle)
admin.site.register(Estado)
admin.site.register(EstadoCivil)
admin.site.register(CategoriaCliente)
admin.site.register(CategoriaViaje)
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
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ViajeHistorial)
admin.site.register(Trayecto)
admin.site.register(CentroCosto)
admin.site.register(Tarifario)
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
admin.site.register(MailPersona)
admin.site.register(MailCliente)
admin.site.register(LicenciaPersona)
admin.site.register(LicenciaVehiculo)
admin.site.register(ViajePasajero)
admin.site.register(AdjuntoViaje)
admin.site.register(TipoPersona)
admin.site.register(Permission)