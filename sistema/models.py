# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Iva(models.Model):
    iva = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.iva

    def __str__(self):
        return self.iva

class CondicionPago(models.Model):
    condicion_pago = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.condicion_pago

    def __str__(self):
        return self.condicion_pago

class Estado(models.Model):
    estado = models.CharField(max_length=50)
    color = models.CharField(max_length=50, null=True, blank=True)

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
    iva_flag = models.BooleanField(default=False)

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
    detalle_tipo_obs = models.CharField(max_length=50,null=True, blank=True)
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

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.CharField(max_length=8, null=True, blank=True)
    documento = models.CharField(max_length=20, null=True, blank=True)
    cuil = models.CharField(max_length=20, null=True, blank=True)
    tipo_persona = models.ForeignKey(TipoPersona, null=True, blank=True)
    estado_civil = models.ForeignKey(EstadoCivil, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    mail = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    iva = models.CharField(max_length=100, null=True, blank=True)
    condicion_pago = models.CharField(max_length=100, null=True, blank=True)
    cbu = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    dias_fechas_facturas = models.CharField(max_length=20, null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.nombre + " " + self.apellido

    def __str__(self):
        return self.nombre + " " + self.apellido

    def nombreCompleto(self):
        return self.nombre + " " + self.apellido

    def getIdentificacion(self):
        return self.nombre + " " + self.apellido

    def getObservaciones(self):
        observaciones = []
        for obspe in self.observacionpersona_set.all():
            observaciones.append(obspe.observacion)
        return observaciones

    def getObservacion(self):
        for obspe in self.observacionpersona_set.all():
            return obspe.observacion.texto
        return ""

    def getLicencias(self):
        licencias = []
        for licper in self.licenciapersona_set.all():
            licencias.append(licper.licencia)
        return licencias

    def getCliente(self):
        if len(self.personacliente_set.all()) > 0:
            return self.personacliente_set.all()[0].cliente.razon_social
        else:
            return 'Sin cliente'

    def getTelefono(self):
        return self.telefono

    def getMail(self):
        return self.mail

    def getDomicilio(self):
        return self.direccion

    def getUnidad(self):
        unidad = Unidad()
        if self.tipo_persona.id == 3:
            unidades = Unidad.objects.filter(chofer__id=self.id)
        if self.tipo_persona.id == 4:
            unidades = Unidad.objects.filter(owner__id=self.id)
        elif  self.tipo_persona.id == 2 or self.tipo_persona.id == 1:
            unidades = ""
        if len(unidades) > 0:
            unidad = unidades[0]
        return unidad

    def getNacimiento(self):
        return getFecha(self.fecha_nacimiento)


class Vehiculo(models.Model):
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=50)
    ano = models.CharField(max_length=10,null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    puertas = models.CharField(max_length=2, null=True, blank=True)
    patente = models.CharField(max_length=20, null=True, blank=True)
    nro_motor = models.CharField(max_length=20, null=True, blank=True)
    nro_chasis = models.CharField(max_length=30, null=True, blank=True)
    dueno = models.ForeignKey(Persona, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nro_motor

    def __str__(self):
        return self.nro_motor

    def getLicencias(self):
        licencias = []
        for licveh in self.licenciavehiculo_set.all():
            licencias.append(licveh.licencia)
        return licencias

    def getIdentificacion(self):
        return self.patente

class Tarifario(models.Model):
    nombre = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

    def getTarifaViaje(self):
        return self.tarifatrayecto_set.all()

    def getTarifaExtra(self):
        return self.tarifaextra_set.all()

class Unidad(models.Model):
    id_fake = models.CharField(max_length=10, null=True, blank=True)
    identificacion = models.CharField(max_length=50)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True)
    baja = models.BooleanField(default=False)
    unidad_propia = models.BooleanField(default=False)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)

    calle = models.CharField(max_length=100, null=True, blank=True)
    documento = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=8, null=True, blank=True)
    mail = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.identificacion

    def __str__(self):
        return self.identificacion

    def getIdVehiculo(self):
        try:
            return self.vehiculo.id
        except Exception as inst:
            return ""

    def getIdTarifario(self):
        try:
            return self.tarifario.id
        except Exception as inst:
            return ""

    def getObservaciones(self):
        observaciones = []
        for obscli in self.observacionunidad_set.all():
            observaciones.append(obscli.observacion)
        return observaciones

    def getLicencias(self):
        return self.licencia_set.all()

    def getFechaNacimiento(self):
        return getFecha(self.fecha_nacimiento)

    class Meta:
        verbose_name_plural = "Unidades"

class Licencia(models.Model):
    comentario = models.CharField(max_length=200, null=True, blank=True)
    tipo_licencia = models.ForeignKey(TipoLicencia, null=True, blank=True)
    fecha_vencimiento = models.CharField(max_length=8, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.fecha_vencimiento

    def __str__(self):
        return self.fecha_vencimiento

    def getFechaVencimiento(self):
        return getFecha(self.fecha_vencimiento)

class Cliente(models.Model):
    razon_social = models.CharField(max_length=60)
    calle = models.CharField(max_length=50, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    piso = models.CharField(max_length=10, null=True, blank=True)
    depto = models.CharField(max_length=10, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    cuil = models.CharField(max_length=11, null=True, blank=True)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    iva = models.ForeignKey(Iva, null=True, blank=True)
    condicion_pago = models.ForeignKey(CondicionPago, null=True, blank=True)
    cbu = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
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

    def getContactos(self):
        contacto = []
        for percli in self.personacliente_set.all():
            if percli.persona.tipo_persona.id == 1 and not percli.persona.baja:
                contacto.append(percli.persona)
        return contacto

    def getPasajeros(self):
        pasajeros = []
        for percli in self.personacliente_set.all():
            if percli.persona.tipo_persona.id == 2 and not percli.persona.baja:
                pasajeros.append(percli.persona)
        return pasajeros

    def getCentroCostos(self):
        cc = []
        for c in self.centrocosto_set.all():
            cc.append(c)
        return cc

    def getTelefonos(self):
        telefono = []
        for telcli in self.telefonocliente_set.all():
            if telcli.telefono.tipo_telefono.id == 1:
                telefono.append(telcli.telefono)
        return telefono

class CentroCosto(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.CharField(max_length=8, null=True, blank=True)
    fecha_fin = models.CharField(max_length=8, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % str(self.id)+"-"+self.nombre

    def __str__(self):
        return str(self.id)+"-"+self.nombre

    def getFechaInicio(self):
        return getFecha(self.fecha_inicio)

    def getFechaFin(self):
        return getFecha(self.fecha_fin)

class TipoPagoViaje(models.Model):
    tipo_pago_viaje = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.tipo_pago_viaje

    def __str__(self):
        return self.tipo_pago_viaje

class UsrUnidad (models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.usuario

    def __str__(self):
        return self.usuario

class UsrCliente (models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.usuario

    def __str__(self):
        return self.usuario

class Viaje(models.Model):
    estado = models.ForeignKey(Estado, null=True, blank=True)
    fecha = models.CharField(max_length=12)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)
    hora = models.CharField(max_length=10, null=True, blank=True)
    solicitante = models.ForeignKey(Persona, related_name='solicitante', null=True, blank=True)
    pasajero = models.ForeignKey(Persona, related_name='pasajero', null=True, blank=True)
    centro_costo = models.ForeignKey(CentroCosto, null=True, blank=True)
    categoria_viaje = models.ForeignKey(CategoriaViaje, null=True, blank=True)
    hora_estimada = models.CharField(max_length=10, null=True, blank=True)
    Cod_ext_viaje = models.CharField(max_length=30, null=True, blank=True)
    tarifapasada = models.CharField(max_length=50, null=True, blank=True)
    nro_aux = models.CharField(max_length=30, null=True, blank=True)
    tipo_pago = models.ForeignKey(TipoPagoViaje, null=True, blank=True, default=1)
    calculo_admin = models.BooleanField(default=False)
    creadopor = models.ForeignKey(User, null=True, blank=True, default=1)
    creadofecha = models.CharField(max_length=12, default=1)
    nropasajeros = models.CharField(max_length=2, default=1)

    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    def getHora(self):
        if "PM" in self.hora:
            hora = self.hora.split(':')[0].replace("1","13").replace("2","14").replace("3","15").replace("4","16").replace("5","17").replace("6","18").replace("7","19").replace("8","20").replace("9","21").replace("10","22").replace("11","23")
            hora = hora + ':' + self.hora.split(':')[1]
            return hora.replace("PM","")
        else:
            return self.hora.replace("AM","")

    def getObservaciones(self):
        observaciones = []
        for obsviaje in self.observacionviaje_set.all():
            observaciones.append(obsviaje.observacion)
        return observaciones

    def getObservacioneChofer(self):
        obs_chofer = ''
        for obsviaje in self.observacionviaje_set.all():
            if obsviaje.observacion.tipo_observacion_id == 17:
                obs_chofer = obsviaje.observacion.texto
        return obs_chofer

    def getViajeItems(self):
        viaje_items = []
        for item in self.itemviaje_set.all():
            viaje_items.append(item)
        return viaje_items

    def getViajeBilingue(self):
        viaje_bilingue = ''
        for item in self.itemviaje_set.all():
            if item.tipo_items_viaje_id == 9:
                viaje_bilingue = '(Bi)'
        return viaje_bilingue

    def getViajeAdjuntos(self):
        viaje_adjuntos = []
        for adjunto in self.adjuntoviaje_set.all():
            viaje_adjuntos.append(adjunto)
        return viaje_adjuntos

    def getTrayectoPrincipal(self):
        try:
            return self.trayecto_set.filter()[:1].get()
        except Trayecto.DoesNotExist:
            return ''

    def getTrayectos(self):
        viaje_trayectos = []
        for trayecto in self.trayecto_set.all():
            print trayecto
            viaje_trayectos.append(trayecto)
        return viaje_trayectos

    def getProforma(self):
        if self.facturaviaje_set.all():
            if self.facturaviaje_set.all()[0].prof_cliente:
                return self.facturaviaje_set.all()[0].prof_cliente
            else:
                return ""
        else:
            return ""

    def getFacturaCliente(self):
        if self.facturaviaje_set.all():
            if self.facturaviaje_set.all()[0].fact_cliente:
                return self.facturaviaje_set.all()[0].fact_cliente
            else:
                return ""
        else:
            return ""

    def getFacturaProveedor(self):
        if self.facturaviaje_set.all():
            if self.facturaviaje_set.all()[0].fact_proveedor:
                return self.facturaviaje_set.all()[0].fact_proveedor
            else:
                return ""
        else:
            return ""

    def getFecha(self):
        return getFecha(self.fecha)

    def getCantidadTiempoEsperaCliente(self):
        retorno = 0
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 1:
                retorno = retorno + iv.cant
        return retorno

    def getMontoTiempoEsperaCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 1:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoBilingueCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 3:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoMontoCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 4:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoPeajesCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 6:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoEstacionCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 5:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoOtrosCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 17:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoPeftCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 12:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getSubtotalCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 2 or iv.tipo_items_viaje.id == 18:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getTotalCliente(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 2 or iv.tipo_items_viaje.id == 18 or iv.tipo_items_viaje.id == 1 or iv.tipo_items_viaje.id == 3 or iv.tipo_items_viaje.id == 4 or iv.tipo_items_viaje.id == 5 or iv.tipo_items_viaje.id == 6 or iv.tipo_items_viaje.id == 17:
                retorno = retorno + iv.monto_s_iva
        return retorno - self.getMontoPeftCliente()

    def getIvaCliente(self):
        retorno = 0.00
        if self.categoria_viaje.iva_flag:
            for iv in self.itemviaje_set.all():
                if iv.tipo_items_viaje.id == 2 or iv.tipo_items_viaje.id == 18 or iv.tipo_items_viaje.id == 1 or iv.tipo_items_viaje.id == 3 or iv.tipo_items_viaje.id == 4 or iv.tipo_items_viaje.id == 5 or iv.tipo_items_viaje.id == 6 or iv.tipo_items_viaje.id == 17:
                    retorno = retorno + iv.monto_iva
        return retorno

    def getFinalCliente(self):
        retorno = self.getTotalCliente() + self.getIvaCliente()
        if self.tipo_pago.id==2:
            retorno = retorno * 1.05
        return retorno

    def getPasajeros(self):
        pasajeros = []
        for pervi in self.viajepasajero_set.all():
            pasajeros.append(pervi.pasajero)
        return pasajeros

    #items proveedor
    def getCantidadTiempoEsperaProveedor(self):
        retorno = 0
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 14:
                retorno = retorno + iv.cant
        return retorno

    def getMontoTiempoEsperaProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 14:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoBilingueProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 9:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoMaletasProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 10:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoPeajesProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 15:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoEstacionProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 11:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getMontoOtrosProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 16:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getCobradoProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 12:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getSubtotalProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 8 or iv.tipo_items_viaje.id == 13:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getTotalProveedor(self):
        retorno = 0.00
        for iv in self.itemviaje_set.all():
            if iv.tipo_items_viaje.id == 8 or iv.tipo_items_viaje.id == 14 or iv.tipo_items_viaje.id == 9 or iv.tipo_items_viaje.id == 10 or iv.tipo_items_viaje.id == 15 or iv.tipo_items_viaje.id == 11 or iv.tipo_items_viaje.id == 16 or iv.tipo_items_viaje.id == 13:
                retorno = retorno + iv.monto_s_iva
        return retorno

    def getIvaProveedor(self):
        retorno = 0.00
        if self.categoria_viaje.iva_flag:
            for iv in self.itemviaje_set.all():
                if iv.tipo_items_viaje.id == 8 or iv.tipo_items_viaje.id == 14 or iv.tipo_items_viaje.id == 9 or iv.tipo_items_viaje.id == 10 or iv.tipo_items_viaje.id == 15 or iv.tipo_items_viaje.id == 11 or iv.tipo_items_viaje.id == 16  or iv.tipo_items_viaje.id == 13:
                    retorno = retorno + iv.monto_iva
        return retorno

    def getFinalProveedor(self):
        retorno = self.getTotalProveedor() + self.getIvaProveedor()
        return retorno

    def getPagarProveedor(self):
        retorno = self.getFinalProveedor() - self.getCobradoProveedor()
        return retorno

    class Meta:
        verbose_name_plural = "Viajes"

class TipoItemViaje(models.Model):
    item_desc = models.CharField(max_length=30, null=True, blank=True)
    iva_pct = models.FloatField(default=0)
    cliente_proveedor = models.CharField(max_length=1, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.item_desc

    def __str__(self):
        return self.item_desc

class ItemViaje(models.Model):
    viaje = models.ForeignKey(Viaje)
    tipo_items_viaje = models.ForeignKey(TipoItemViaje)
    monto = models.FloatField(default=0)
    monto_iva = models.FloatField(default=0)
    monto_s_iva = models.FloatField(default=0)
    cant = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.viaje

    def __str__(self):
        return self.viaje

class FacturaViaje(models.Model):
    viaje = models.ForeignKey(Viaje)
    fact_cliente = models.CharField(max_length=30, null=True, blank=True)
    prof_cliente = models.CharField(max_length=30, null=True, blank=True)
    fact_proveedor = models.CharField(max_length=30, null=True, blank=True)


    def __unicode__(self):
        return u'%s' % self.viaje

    def __str__(self):
        return self.viaje

class ViajePasajero(models.Model):
    viaje = models.ForeignKey(Viaje)
    pasajero = models.ForeignKey(Persona, null=True, blank=True)
    pasajero_ppal = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.pasajero

    def __str__(self):
        return self.pasajero

    class Meta:
        verbose_name_plural = "Pasajero Viaje"

class ViajeHistorial(models.Model):
    viaje = models.ForeignKey(Viaje, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    fecha = models.CharField(max_length=12)
    valor_anterior = models.CharField(max_length=200)
    valor_actual = models.CharField(max_length=200)
    campo_modificado = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.campo_modificado

    def __str__(self):
        return self.campo_modificado

    def getFecha(self):
        return getFecha(self.fecha)

    class Meta:
        verbose_name_plural = "Historial de viajes"

class TrayectoDestino(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    terminal_flag = models.BooleanField(default=False)
    color = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    trayectodestino = models.ForeignKey(TrayectoDestino, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=50)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    id_externo = models.CharField(max_length=50, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    trayectodestino = models.ForeignKey(TrayectoDestino, null=True, blank=True)
    terminal_flag = models.BooleanField(default=False)
    color = models.CharField(max_length=20, null=True)
    baja = models.BooleanField(default=False)

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

class TarifaExtra(models.Model):
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    extra_descripcion = models.CharField(max_length=40, null=True, blank=True)
    baja = models.BooleanField(default=False)
    cat1 = models.FloatField(default=0)
    cat2 = models.FloatField(default=0)
    cat3 = models.FloatField(default=0)
    cat4 = models.FloatField(default=0)
    cat5 = models.FloatField(default=0)
    cat6 = models.FloatField(default=0)
    cat7 = models.FloatField(default=0)
    cat8 = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s' % self.extra_descripcion

    def __str__(self):
        return self.extra_descripcion

    def getTarifaExtraByCategoria(self, idCat):
        retorno = 0
        if idCat == 1:
            retorno = self.cat1
        if idCat == 2:
            retorno = self.cat2
        if idCat == 3:
            retorno = self.cat3
        if idCat == 4:
            retorno = self.cat4
        if idCat == 5:
            retorno = self.cat5
        if idCat == 6:
            retorno = self.cat6
        if idCat == 7:
            retorno = self.cat7
        if idCat == 8:
            retorno = self.cat8
        return str(retorno)

    def getTTPByCategoria(self, idCat):
        retorno = TarifaExtraPrecio()
        for ttp in self.tarifaextraprecio_set.all():
            if ttp.categoria_viaje.id == idCat:
                return ttp
        cat = CategoriaViaje.objects.get(id=idCat)
        retorno.tarifa_extra = self
        retorno.categoria_viaje = cat
        return retorno

class TarifaTrayecto(models.Model):
    descripcion = models.CharField(max_length=50)
    localidad_desde = models.ForeignKey(Localidad, related_name='desde_loc', null=True, blank=True)
    localidad_hasta = models.ForeignKey(Localidad, related_name='hasta_loc', null=True, blank=True)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    baja = models.BooleanField(default=False)
    cat1 = models.FloatField(default=0)
    cat2 = models.FloatField(default=0)
    cat3 = models.FloatField(default=0)
    cat4 = models.FloatField(default=0)
    cat5 = models.FloatField(default=0)
    cat6 = models.FloatField(default=0)
    cat7 = models.FloatField(default=0)
    cat8 = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s' % self.descripcion

    def __str__(self):
        return self.descripcion

    def getTarifaByCategoria(self, idCat):
        retorno = 0
        if idCat == 1:
            retorno = self.cat1
        if idCat == 2:
            retorno = self.cat2
        if idCat == 3:
            retorno = self.cat3
        if idCat == 4:
            retorno = self.cat4
        if idCat == 5:
            retorno = self.cat5
        if idCat == 6:
            retorno = self.cat6
        if idCat == 7:
            retorno = self.cat7
        if idCat == 8:
            retorno = self.cat8
        return str(retorno)

    def getTTPByCategoria(self, idCat):
        retorno = TarifaTrayectoPrecio()
        for ttp in self.tarifatrayectoprecio_set.all():
            if ttp.categoria_viaje.id == idCat:
                return ttp
        cat = CategoriaViaje.objects.get(id=idCat)
        retorno.tarifatrayecto = self
        retorno.categoria_viaje = cat
        return retorno

class Trayecto(models.Model):
    viaje = models.ForeignKey(Viaje, null=True, blank=True)
    calle_desde = models.CharField(max_length=100, null=True, blank=True)
    altura_desde = models.CharField(max_length=10, null=True, blank=True)
    entre_desde = models.CharField(max_length=80, null=True, blank=True)
    localidad_desde = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_desde')
    provincia_desde = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_desde')
    compania_desde = models.CharField(max_length=30, null=True, blank=True)
    vuelo_desde = models.CharField(max_length=20, null=True, blank=True)
    destino_desde = models.ForeignKey(TrayectoDestino, null=True, blank=True, related_name='destino_desde')
    calle_hasta = models.CharField(max_length=100, null=True, blank=True)
    altura_hasta = models.CharField(max_length=20, null=True, blank=True)
    entre_hasta = models.CharField(max_length=80, null=True, blank=True)
    localidad_hasta = models.ForeignKey(Localidad, null=True, blank=True, related_name='localidad_hasta')
    provincia_hasta = models.ForeignKey(Provincia, null=True, blank=True, related_name='provincia_hasta')
    compania_hasta = models.CharField(max_length=30, null=True, blank=True)
    vuelo_hasta = models.CharField(max_length=20, null=True, blank=True)
    destino_hasta = models.ForeignKey(TrayectoDestino, null=True, blank=True, related_name='destino_hasta')
    pasajero = models.ForeignKey(Persona, null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
    tramoppalflag = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.calle_desde

    def __str__(self):
        return self.calle_desde

    def desdeConcat(self):
        retorno = ""

        if self.destino_desde:
            retorno = self.destino_desde.nombre + ", "
        if self.provincia_desde:
            retorno += self.provincia_desde.nombre + ", "
        if self.localidad_desde:
            retorno += self.localidad_desde.nombre + ", "
        if self.calle_desde:
            retorno += self.calle_desde + " " + self.altura_desde + ", "
        if self.compania_desde:
            retorno += self.compania_desde + ", "
        if self.vuelo_desde:
            retorno += self.vuelo_desde + ", "
        if self.entre_desde:
            retorno += self.entre_desde + ", "
        return retorno[:-2]


    def hastaConcat(self):
        retorno = ""

        if self.destino_hasta:
            retorno = self.destino_hasta.nombre + ", "
        if self.provincia_hasta:
            retorno += self.provincia_hasta.nombre + ", "
        if self.localidad_hasta:
            retorno += self.localidad_hasta.nombre + ", "
        if self.calle_hasta:
            retorno += self.calle_hasta + " " + self.altura_hasta + ", "
        if self.compania_hasta:
            retorno += self.compania_hasta + ", "
        if self.vuelo_hasta:
            retorno += self.vuelo_hasta + ", "
        if self.entre_hasta:
            retorno += self.entre_hasta + ", "
        return retorno[:-2]

class OperacionesConfCol(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True)
    orden = models.CharField(max_length=10, null=True, blank=True)
    col_name = models.CharField(max_length=50, null=True, blank=True)
    vista = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.col_name

    def __str__(self):
        return self.col_name

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

class TipoAdelanto (models.Model):
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    logica = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.descripcion

    def __str__(self):
        return self.descripcion

class Adelanto (models.Model):
    unidad = models.ForeignKey(Unidad, null=True, blank=True)
    tipo_adelanto = models.ForeignKey(TipoAdelanto, null=True, blank=True)
    fecha = models.CharField(max_length=8, null=True, blank=True)
    monto = models.CharField(max_length=25, null=True, blank=True)
    factura = models.CharField(max_length=25, null=True, blank=True)
    descripcion = models.CharField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.unidad

    def __str__(self):
        return self.unidad

    def getFecha(self):
        return getFecha(self.fecha)

# devuelve hh:mm dd/mm/aaaa
def getFechaHora(aaaammddhhmm):
    if aaaammddhhmm == None:
        return ""
    return aaaammddhhmm[8:10] + ":" + aaaammddhhmm[10:12] + " " + aaaammddhhmm[6:8] + "/" + aaaammddhhmm[4:6] + "/" + aaaammddhhmm[0:4]

def getFecha(aaaammdd):
    if aaaammdd == None:
        return ""
    return aaaammdd[6:8] + "/" + aaaammdd[4:6] + "/" + aaaammdd[0:4]
