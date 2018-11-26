# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import *

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
    list_display = ('estado', 'getFecha', 'cliente', 'unidad', 'categoria_viaje')

class ClienteAdmin(admin.ModelAdmin):
    inlines = [
        PersonaClienteInline,
    ]
    list_display = ('id', 'razon_social',)

admin.site.register(Viaje, ViajeAdmin)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Calle)
admin.site.register(Estado)
admin.site.register(EstadoCivil)
admin.site.register(CategoriaViaje)
admin.site.register(TipoObservacion)
admin.site.register(TipoLicencia)
admin.site.register(TipoTelefono)
admin.site.register(Adjunto)
admin.site.register(Telefono)
admin.site.register(Observacion)
admin.site.register(Mail)
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
admin.site.register(TelefonoPersona)
admin.site.register(TelefonoCliente)
admin.site.register(MailPersona)
admin.site.register(MailCliente)
admin.site.register(LicenciaPersona)
admin.site.register(LicenciaVehiculo)
admin.site.register(ViajePasajero)
admin.site.register(AdjuntoViaje)
admin.site.register(TipoPersona)
admin.site.register(TrayectoDestino)
admin.site.register(Iva)
admin.site.register(CondicionPago)
admin.site.register(Permission)
admin.site.register(TipoItemViaje)
admin.site.register(ItemViaje)
admin.site.register(FacturaViaje)
admin.site.register(Adelanto)
admin.site.register(TarifaTrayecto)
admin.site.register(TarifaTrayectoPrecio)
admin.site.register(UsrUnidad)
admin.site.register(UsrCliente)
