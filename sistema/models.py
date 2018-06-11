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

class CategoriaViaje(models.Model):
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
    texto = models.TextField()
    tipo_observacion = models.ForeignKey(TipoObservacion, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.fecha

    def __str__(self):
        return self.fecha

    def getFechaHora(self):
        return getFechaHora(self.fecha)

    class Meta:
        verbose_name_plural = "Observaciones" 

class Mail(models.Model):
    mail = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.mail

    def __str__(self):
        return self.mail

class Licencia(models.Model):
    licencia = models.CharField(max_length=100, null=True, blank=True)
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
    contacto_cliente = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    iva = models.CharField(max_length=100, null=True, blank=True)
    condicion_pago = models.CharField(max_length=100, null=True, blank=True)
    cbu = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    dias_fechas_facturas = models.CharField(max_length=20, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

    def nombreCompleto(self):
        return self.nombre + " " + self.apellido

    def getObservaciones(self):
        observaciones = []
        for obspe in self.observacionpersona_set.all():
            observaciones.append(obspe.observacion)
        return observaciones

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
    porcentaje_chofer = models.CharField(max_length=20, null=True, blank=True)
    porcentaje_owner = models.CharField(max_length=20, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.identificacion

    def __str__(self):
        return self.identificacion

    def getIdChofer(self):
        try:
            return self.chofer.id
        except Exception as inst:
            return ""

    def getIdOwner(self):
        try:
            return self.owner.id
        except Exception as inst:
            return ""

    def getObservaciones(self):
        observaciones = []
        for obscli in self.observacionunidad_set.all():
            observaciones.append(obscli.observacion)
        return observaciones

    class Meta:
        verbose_name_plural = "Unidades" 

class Tarifario(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre
        
class Cliente(models.Model):
    razon_social = models.CharField(max_length=100)
    calle = models.CharField(max_length=100, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    piso = models.CharField(max_length=10, null=True, blank=True)
    depto = models.CharField(max_length=10, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    cuil = models.CharField(max_length=11, null=True, blank=True)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    iva = models.CharField(max_length=100, null=True, blank=True)
    condicion_pago = models.CharField(max_length=100, null=True, blank=True)
    cbu = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    dias_fechas_facturas = models.CharField(max_length=20, null=True, blank=True)
    baja = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.razon_social

    def __str__(self):
        return self.razon_social

    def telefonoPrincipal(self):
        retorno = "Sin telefono."
        if len(self.telefonocliente_set.all()) > 0:
            for tel in self.telefonocliente_set.all():
                if tel.telefono.tipo_telefono.tipo_telefono == "Principal":
                    retorno = tel.telefono.numero
        return retorno

    def getObservaciones(self):
        observaciones = []
        for obscli in self.observacioncliente_set.all():
            observaciones.append(obscli.observacion)
        return observaciones

    def getMails(self):
        mails = []
        for mailcli in self.mailcliente_set.all():
            mails.append(mailcli.mail)
        return mails

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
    hora = models.CharField(max_length=10, null=True, blank=True)
    solicitante = models.CharField(max_length=50, null=True, blank=True)
    pasajero = models.CharField(max_length=50, null=True, blank=True)
    centro_costo = models.ForeignKey(CentroCosto, null=True, blank=True)
    categoria_viaje = models.ForeignKey(CategoriaViaje, null=True, blank=True)
    hora_estimada = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    def getTrayectoPrincipal(self):
        trayecto = self.trayecto_set.filter()[:1].get()
        return trayecto

    class Meta:
        verbose_name_plural = "Viajes" 

class ViajePasajero(models.Model):
    viaje = models.ForeignKey(Viaje)
    pasajero = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.pasajero

    def __str__(self):
        return self.pasajero

    class Meta:
        verbose_name_plural = "Pasajero Viaje" 

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

class TipoTrayectoDestino(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class TrayectoDestino(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    tipo_trayecto_destino = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Trayecto(models.Model):
    viaje = models.ForeignKey(Viaje, null=True, blank=True)
    calle_desde = models.CharField(max_length=100, null=True, blank=True)
    altura_desde = models.CharField(max_length=10, null=True, blank=True)
    entre_desde = models.CharField(max_length=100, null=True, blank=True)
    localidad_desde = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_desde')
    provincia_desde = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_desde')
    compania_desde = models.CharField(max_length=30, null=True, blank=True)
    vuelo_desde = models.CharField(max_length=30, null=True, blank=True)
    destino_desde = models.ForeignKey(TrayectoDestino, null=True, blank=True, related_name='destino_desde')
    calle_hasta = models.CharField(max_length=30, null=True, blank=True)
    altura_hasta = models.CharField(max_length=30, null=True, blank=True)
    entre_hasta = models.CharField(max_length=30, null=True, blank=True)
    localidad_hasta = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_hasta')
    provincia_hasta = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_hasta')
    compania_hasta = models.CharField(max_length=30, null=True, blank=True)
    vuelo_hasta = models.CharField(max_length=30, null=True, blank=True)
    destino_hasta = models.ForeignKey(TrayectoDestino, null=True, blank=True, related_name='destino_hasta')
    base_tot = models.CharField(max_length=30, null=True, blank=True)
    peaje_tot = models.CharField(max_length=30, null=True, blank=True)
    estacionamiento_tot = models.CharField(max_length=30, null=True, blank=True)
    otros_tot = models.CharField(max_length=30, null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.calle_desde

    def __str__(self):
        return self.calle_desde

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
    telefono = models.ForeignKey(Telefono, null=True, blank=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.telefono

    def __str__(self):
        return self.telefono

class MailPersona(models.Model):
    mail = models.ForeignKey(Mail, null=True, blank=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.mail

    def __str__(self):
        return self.mail 

class MailCliente(models.Model):
    mail = models.ForeignKey(Mail, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.mail

    def __str__(self):
        return self.mail 

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

class LicenciaPersona(models.Model):
    licencia = models.ForeignKey(Licencia, null=True, blank=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.licencia

    def __str__(self):
        return self.licencia

class LicenciaVehiculo(models.Model):
    licencia = models.ForeignKey(Licencia, null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.licencia

    def __str__(self):
        return self.licencia

# devuelve hh:mm dd/mm/aaaa
def getFechaHora(aaaammddhhmm):
    return aaaammddhhmm[8:10] + ":" + aaaammddhhmm[10:12] + " " + aaaammddhhmm[6:8] + "/" + aaaammddhhmm[4:6] + "/" + aaaammddhhmm[0:4]