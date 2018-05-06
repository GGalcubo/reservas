# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Calle(models.Model):
    nombre = models.CharField(max_length=100)
    altura_desde = models.CharField(max_length=10, null=True, blank=True)
    altura_hasta  = models.CharField(max_length=10, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    estado = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.estado

    def __str__(self):
        return self.estado

class EstadoCivil(models.Model):
    estado_civil = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.estado_civil

    def __str__(self):
        return self.estado_civil

class CategoriaCliente(models.Model):
    categoria = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.categoria

    def __str__(self):
        return self.categoria

class CategoriaUnidad(models.Model):
    codigo = models.CharField(max_length=10, null=True, blank=True)
    categoria = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.categoria

    def __str__(self):
        return self.categoria

class TipoPersona(models.Model):
    tipo_persona = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.tipo_persona

    def __str__(self):
        return self.tipo_persona

class TipoObservacion(models.Model):
    tipo_observacion = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.tipo_observacion

    def __str__(self):
        return self.tipo_observacion

class TipoLicencia(models.Model):
    tipo_licencia = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.tipo_licencia

    def __str__(self):
        return self.tipo_licencia

class Adjunto(models.Model):
    upload = models.FileField(upload_to='adjuntos/')
    fecha = models.CharField(max_length=12)
    observacion = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.upload

    def __str__(self):
        return self.upload

class TipoTelefono(models.Model):
    tipo_telefono = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.tipo_telefono

    def __str__(self):
        return self.tipo_telefono

class Telefono(models.Model):
    tipo_telefono = models.ForeignKey(TipoTelefono, null=True, blank=True)
    numero = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.numero

    def __str__(self):
        return self.numero

class Observacion(models.Model):
    fecha = models.CharField(max_length=12)
    observacion = models.TextField()
    tipo_observacion = models.ForeignKey(TipoObservacion, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

    class Meta:
        verbose_name_plural = "Observaciones" 

class Licencia(models.Model):
    tipo_licencia = models.ForeignKey(TipoLicencia, null=True, blank=True)
    fecha_vencimiento = models.CharField(max_length=8, null=True, blank=True)
    numero = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.numero

    def __str__(self):
        return self.numero

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.CharField(max_length=8, null=True, blank=True)
    documento = models.CharField(max_length=8, null=True, blank=True)
    tipo_persona = models.ForeignKey(TipoPersona, null=True, blank=True)
    porcentaje_viaje = models.CharField(max_length=3, null=True, blank=True)
    estado_civil = models.ForeignKey(EstadoCivil, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    piso = models.CharField(max_length=10, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    mail = models.CharField(max_length=100, null=True, blank=True)
    porcentaje_viaje = models.IntegerField(default=0)
    contacto_cliente = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    licencia = models.ForeignKey(Licencia, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=10)
    color = models.CharField(max_length=50, null=True, blank=True)
    puertas = models.CharField(max_length=10, null=True, blank=True)
    patente = models.CharField(max_length=100, null=True, blank=True)
    nro_motor = models.CharField(max_length=100, null=True, blank=True)
    nro_chasis = models.CharField(max_length=100, null=True, blank=True)
    licencia = models.ForeignKey(Licencia, null=True, blank=True)
    dueno = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nro_motor

    def __str__(self):
        return self.nro_motor

class Unidad(models.Model):
    identificacion = models.CharField(max_length=100)
    chofer = models.ForeignKey(Persona, related_name='chofer', null=True, blank=True)
    owner = models.ForeignKey(Persona, related_name='owner', null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.identificacion

    def __str__(self):
        return self.identificacion

    class Meta:
        verbose_name_plural = "Unidades" 

class Cliente(models.Model):
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    cuil = models.CharField(max_length=11, null=True, blank=True)
    categoria = models.ForeignKey(CategoriaCliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.razon_social

    def __str__(self):
        return self.razon_social

class Viaje(models.Model):
    factura = models.CharField(max_length=30, null=True, blank=True)
    proforma = models.CharField(max_length=30, null=True, blank=True)
    estado = models.ForeignKey(Estado, null=True, blank=True)
    fecha = models.CharField(max_length=12)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)
    base_total = models.IntegerField(default=0)
    peaje_total = models.IntegerField(default=0)
    estacionamiento_total = models.IntegerField(default=0)
    Otros_tot = models.IntegerField(default=0)
    maletas = models.BooleanField(default=False)
    bilingue = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    class Meta:
        verbose_name_plural = "Viajes" 

class ViajeHistorial(models.Model):
    viaje = models.ForeignKey(Viaje, null=True, blank=True)
    usuario = models.OneToOneField(User)
    fecha = models.CharField(max_length=12)
    valor_anterior = models.CharField(max_length=100)
    valor_actual = models.CharField(max_length=100)
    campo_modificado = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.campo_modificado

    def __str__(self):
        return self.campo_modificado

    class Meta:
        verbose_name_plural = "Historial de viajes" 

class Trayecto(models.Model):
    viaje = models.ForeignKey(Viaje, null=True, blank=True)
    calle_desde = models.CharField(max_length=100, null=True, blank=True)
    altura_desde = models.CharField(max_length=10, null=True, blank=True)
    entre_desde = models.CharField(max_length=100, null=True, blank=True)
    localidad_desde = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_desde')
    provincia_desde = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_desde')
    compania_desde = models.CharField(max_length=30, null=True, blank=True)
    vuelo_desde = models.CharField(max_length=30, null=True, blank=True)
    destino_desde = models.CharField(max_length=30, null=True, blank=True)
    calle_hasta = models.CharField(max_length=30, null=True, blank=True)
    altura_hasta = models.CharField(max_length=30, null=True, blank=True)
    entre_hasta = models.CharField(max_length=30, null=True, blank=True)
    localidad_hasta = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_hasta')
    provincia_hasta = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_hasta')
    compania_hasta = models.CharField(max_length=30, null=True, blank=True)
    vuelo_hasta = models.CharField(max_length=30, null=True, blank=True)
    destino_hasta = models.CharField(max_length=30, null=True, blank=True)
    base_tot = models.CharField(max_length=30, null=True, blank=True)
    peaje_tot = models.CharField(max_length=30, null=True, blank=True)
    estacionamiento_tot = models.CharField(max_length=30, null=True, blank=True)
    otros_tot = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.calle_desde

    def __str__(self):
        return self.calle_desde

class CentroCosto(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.CharField(max_length=8, null=True, blank=True)
    fecha_fin = models.CharField(max_length=8, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Tarifario(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class PersonaCliente(models.Model):
    persona = models.ForeignKey(Persona, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.persona

    def __str__(self):
        return self.persona

class ObservacionPersona(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionUnidad(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionVehiculo(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionCliente(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionViaje(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    viaje = models.ForeignKey(Viaje, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionCentroCosto(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    centro_costo = models.ForeignKey(CentroCosto, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionLicencia(models.Model):
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    licencia = models.ForeignKey(Licencia, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion


class TelefonoPersona(models.Model):
    Telefono = models.ForeignKey(Telefono, null=True, blank=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class TelefonoCliente(models.Model):
    telefono = models.ForeignKey(Telefono, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.cliente

    def __str__(self):
        return self.cliente

class AdjuntoViaje(models.Model):
    adjunto = models.ForeignKey(Adjunto, null=True, blank=True)
    viaje = models.ForeignKey(Viaje, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.adjunto

    def __str__(self):
        return self.adjunto