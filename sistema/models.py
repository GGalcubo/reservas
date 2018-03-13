# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Estado(models.Model):
    estado = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.estado

    def __str__(self):
        return self.estado

class CategoriaEmpresa(models.Model):
    categoria = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.categoria

    def __str__(self):
        return self.categoria

class CategoriaVehiculo(models.Model):
    codigo = models.CharField(max_length=10)
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
    observacion = models.TextField()

    def __unicode__(self):
        return u'%s' % self.upload

    def __str__(self):
        return self.upload

class TipoTelefono(models.Model):
    tipo_telefono = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.tipo_telefono

    def __str__(self):
        return self.tipo_obsertipo_telefonotipo_telefonovacion

class Telefono(models.Model):
    tipo_telefono = models.ForeignKey(TipoTelefono)
    numero = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.numero

    def __str__(self):
        return self.numero

class Observacion(models.Model):
    fecha = models.CharField(max_length=12)
    observacion = models.TextField()
    tipo_observacion = models.ForeignKey(TipoObservacion)

    def __unicode__(self):
        return u'%s' % self.estado

    def __str__(self):
        return self.estado

    class Meta:
        verbose_name_plural = "Observaciones" 

class Licencia(models.Model):
    tipo_licencia = models.ForeignKey(TipoLicencia)
    fecha_vencimiento = models.CharField(max_length=8)
    identificador = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.identificador

    def __str__(self):
        return self.identificador

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.CharField(max_length=8)
    documento = models.CharField(max_length=8)
    tipo_persona = models.ForeignKey(TipoPersona)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    puertas = models.CharField(max_length=10)
    patente = models.CharField(max_length=100)
    nro_motor = models.CharField(max_length=100)
    nro_chasis = models.CharField(max_length=100)
    licencia = models.ForeignKey(Licencia)
    dueno = models.ForeignKey(Persona)
    categoria = models.ForeignKey(CategoriaVehiculo)
    licencia_centro = models.CharField(max_length=100)
    vto_licencia_centro = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.nro_motor

    def __str__(self):
        return self.nro_motor

class Empresa(models.Model):
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    cuil = models.CharField(max_length=11)
    categoria = models.ForeignKey(CategoriaEmpresa)
    #tipo_tarifa

class Viaje(models.Model):
    factura = models.CharField(max_length=30, null=True, blank=True)
    proforma = models.CharField(max_length=30, null=True, blank=True)
    estado = models.ForeignKey(Estado)
    fecha = models.CharField(max_length=12)
    empresa = models.ForeignKey(Empresa)
    vehiculo = models.ForeignKey(Vehiculo)
    base_total = models.IntegerField(default=0)
    peaje_total = models.IntegerField()
    estacionamiento_total = models.IntegerField()
    Otros_tot = models.IntegerField()
    maletas = models.CharField(max_length=30)
    bilingue = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    class Meta:
        verbose_name_plural = "Viajes" 

class Trayecto(models.Model):
    viaje = models.ForeignKey(Viaje)
    calle_desde = models.CharField(max_length=100, null=True, blank=True)
    altura_desde = models.CharField(max_length=10, null=True, blank=True)
    entre_desde = models.CharField(max_length=100, null=True, blank=True)
    provincia_desde = models.CharField(max_length=30, null=True, blank=True)
    compania_desde = models.CharField(max_length=30, null=True, blank=True)
    vuelo_desde = models.CharField(max_length=30, null=True, blank=True)
    Localidad_desde = models.CharField(max_length=30, null=True, blank=True)
    Destino_desde = models.CharField(max_length=30, null=True, blank=True)
    calle_hast = models.CharField(max_length=30, null=True, blank=True)
    altura_hast = models.CharField(max_length=30, null=True, blank=True)
    entre_hast = models.CharField(max_length=30, null=True, blank=True)
    provincia_hast = models.CharField(max_length=30, null=True, blank=True)
    compania_hast = models.CharField(max_length=30, null=True, blank=True)
    vuelo_hast = models.CharField(max_length=30, null=True, blank=True)
    Localidad_hast = models.CharField(max_length=30, null=True, blank=True)
    Destino_hast = models.CharField(max_length=30, null=True, blank=True)
    Base_tot = models.CharField(max_length=30, null=True, blank=True)
    Peaje_tot = models.CharField(max_length=30, null=True, blank=True)
    estacionamiento_tot = models.CharField(max_length=30, null=True, blank=True)
    Otros_tot = models.CharField(max_length=30, null=True, blank=True)
    Maletas = models.CharField(max_length=30, null=True, blank=True)
    Bilingue = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.calle_desde

    def __str__(self):
        return self.calle_desde

class PersonaEmpresa(models.Model):
    persona = models.ForeignKey(Persona)
    empresa = models.ForeignKey(Empresa)

    def __unicode__(self):
        return u'%s' % self.persona

    def __str__(self):
        return self.persona

class ObservacionVehiculo(models.Model):
    observacion = models.ForeignKey(Observacion)
    vehiculo = models.ForeignKey(Vehiculo)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionEmpresa(models.Model):
    observacion = models.ForeignKey(Observacion)
    empresa = models.ForeignKey(Empresa)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class ObservacionViaje(models.Model):
    observacion = models.ForeignKey(Observacion)
    viaje = models.ForeignKey(Viaje)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class TelefonoPersona(models.Model):
    Telefono = models.ForeignKey(Telefono)
    persona = models.ForeignKey(Persona)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class TelefonoEmpresa(models.Model):
    telefono = models.ForeignKey(Telefono)
    empresa = models.ForeignKey(Empresa)

    def __unicode__(self):
        return u'%s' % self.observacion

    def __str__(self):
        return self.observacion

class AdjuntoViaje(models.Model):
    adjunto = models.ForeignKey(Adjunto)
    viaje = models.ForeignKey(Viaje)

    def __unicode__(self):
        return u'%s' % self.adjunto

    def __str__(self):
        return self.adjunto