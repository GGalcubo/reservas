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

class Licencia(models.Model):
    comentario = models.CharField(max_length=200, null=True, blank=True)
    tipo_licencia = models.ForeignKey(TipoLicencia, null=True, blank=True)
    fecha_vencimiento = models.CharField(max_length=8, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.fecha_vencimiento

    def __str__(self):
        return self.fecha_vencimiento

    def getFechaVencimiento(self):
        return getFecha(self.fecha_vencimiento)

    def getAsignadoTipo(self):
        if len(self.licenciapersona_set.all()) > 0:
            return self.licenciapersona_set.all()[0].persona.tipo_persona.tipo_persona
        elif len(self.licenciavehiculo_set.all()) > 0:
            return 'Vehiculo'

    def getAsignadoTipoId(self):
        if len(self.licenciapersona_set.all()) > 0:
            if self.licenciapersona_set.all()[0].persona.tipo_persona.id == 3:
                return 0
            elif self.licenciapersona_set.all()[0].persona.tipo_persona.id == 4:
                return 1
        elif len(self.licenciavehiculo_set.all()) > 0:
            return 2

    def getAsignadoNombre(self):
        if len(self.licenciapersona_set.all()) > 0:
            return self.licenciapersona_set.all()[0].persona.nombre + " " + self.licenciapersona_set.all()[0].persona.apellido
        elif len(self.licenciavehiculo_set.all()) > 0:
            return self.licenciavehiculo_set.all()[0].vehiculo.patente

    def getAsignado(self):
        if len(self.licenciapersona_set.all()) > 0:
            return self.licenciapersona_set.all()[0].persona
        elif len(self.licenciavehiculo_set.all()) > 0:
            return self.licenciavehiculo_set.all()[0].vehiculo

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.CharField(max_length=8, null=True, blank=True)
    documento = models.CharField(max_length=20, null=True, blank=True)
    cuil = models.CharField(max_length=20, null=True, blank=True)
    tipo_persona = models.ForeignKey(TipoPersona, null=True, blank=True)
    estado_civil = models.ForeignKey(EstadoCivil, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    piso = models.CharField(max_length=10, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    mail = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    iva = models.CharField(max_length=100, null=True, blank=True)
    condicion_pago = models.CharField(max_length=100, null=True, blank=True)
    cbu = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    dias_fechas_facturas = models.CharField(max_length=20, null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

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
        if len(self.telefonopersona_set.all()) > 0:
            return self.telefonopersona_set.all()[0].telefono.numero
        else:
            return 'Sin telefono'

    def getMail(self):
        if len(self.mailpersona_set.all()) > 0:
            return self.mailpersona_set.all()[0].mail.mail
        else:
            return 'Sin mail'

    def getDomicilio(self):
        retorno = ""
        if self.calle != None:
            retorno = retorno + self.calle
            if self.altura != None:
                retorno = retorno + " "+ self.altura
        return retorno

    def getUnidad(self):
        unidad = Unidad()
        if self.tipo_persona.id == 3:
            unidades = Unidad.objects.filter(chofer__id=self.id)
        elif self.tipo_persona.id == 4:
            unidades = Unidad.objects.filter(owner__id=self.id)
        if len(unidades) > 0:
            unidad = unidades[0]
        return unidad
        

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

class Unidad(models.Model):
    identificacion = models.CharField(max_length=50)
    chofer = models.ForeignKey(Persona, related_name='chofer', null=True, blank=True)
    owner = models.ForeignKey(Persona, related_name='owner', null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True)
    porcentaje_chofer = models.CharField(max_length=20, null=True, blank=True)
    porcentaje_owner = models.CharField(max_length=20, null=True, blank=True)
    baja = models.BooleanField(default=False)
    unidad_propia = models.BooleanField(default=False)

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

    def getIdVehiculo(self):
        try:
            return self.vehiculo.id
        except Exception as inst:
            return ""

    def getObservaciones(self):
        observaciones = []
        for obscli in self.observacionunidad_set.all():
            observaciones.append(obscli.observacion)
        return observaciones

    def getLicencias(self):
        licencias = []
        if self.chofer:
            licencias.extend(self.chofer.getLicencias())
        if self.owner:
            licencias.extend(self.owner.getLicencias())
        if self.vehiculo:
            licencias.extend(self.vehiculo.getLicencias())
        return licencias

    class Meta:
        verbose_name_plural = "Unidades" 

class Tarifario(models.Model):
    nombre = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre
        
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
            if percli.persona.tipo_persona.id == 1:
                contacto.append(percli.persona)
        return contacto

    def getPasajeros(self):
        pasajeros = []
        for percli in self.personacliente_set.all():
            if percli.persona.tipo_persona.id == 2:
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
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

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
        
class Viaje(models.Model):
    estado = models.ForeignKey(Estado, null=True, blank=True)
    fecha = models.CharField(max_length=12)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)
    hora = models.CharField(max_length=10, null=True, blank=True)
    solicitante = models.CharField(max_length=50, null=True, blank=True)
    pasajero = models.CharField(max_length=50, null=True, blank=True)
    centro_costo = models.ForeignKey(CentroCosto, null=True, blank=True)
    categoria_viaje = models.ForeignKey(CategoriaViaje, null=True, blank=True)
    hora_estimada = models.CharField(max_length=10, null=True, blank=True)
    Cod_ext_viaje = models.CharField(max_length=30, null=True, blank=True)
    tarifapasada = models.IntegerField(default=0)
    nro_aux= models.CharField(max_length=30, null=True, blank=True)
    tipo_pago = models.ForeignKey(TipoPagoViaje, null=True, blank=True, default=1)
    
    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    def getObservaciones(self):
        observaciones = []
        for obsviaje in self.observacionviaje_set.all():
            observaciones.append(obsviaje.observacion)
        return observaciones

    def getTrayectoPrincipal(self):
        trayecto = self.trayecto_set.filter()[:1].get()
        return trayecto

    def getFecha(self):
        return getFecha(self.fecha)

    class Meta:
        verbose_name_plural = "Viajes"

class TipoItemViaje(models.Model):
    item_desc = models.CharField(max_length=30, null=True, blank=True)
    iva_pct = models.FloatField(default=0)
    cliente_proveedor = models.CharField(max_length=1, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.viaje.item_desc

    def __str__(self):
        return self.viaje.item_desc  

class ItemViaje(models.Model):
    viaje = models.ForeignKey(Viaje)
    tipo_items_viaje = models.ForeignKey(TipoItemViaje)
    monto_iva = models.FloatField(default=0)
    monto_s_iva = models.FloatField(default=0)
    cant = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.viaje.viaje

    def __str__(self):
        return self.viaje.viaje   

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
    pasajero = models.CharField(max_length=100)

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
    valor_anterior = models.CharField(max_length=100)
    valor_actual = models.CharField(max_length=100)
    campo_modificado = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.campo_modificado

    def __str__(self):
        return self.campo_modificado

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
    extra_precio = models.CharField(max_length=20, null=True, blank=True)
    extra_precio_prov= models.CharField(max_length=20, null=True, blank=True)
    categoria_viaje = models.ForeignKey(CategoriaViaje, null=True, blank=True)
    

    def __unicode__(self):
        return u'%s' % self.extra_descripcion

    def __str__(self):
        return self.extra_descripcion

class TarifaViaje(models.Model):
    descripcion = models.CharField(max_length=50)
    localidad_desde = models.ForeignKey(Localidad, related_name='desde_loc', null=True, blank=True)
    localidad_hasta = models.ForeignKey(Localidad, related_name='hasta_loc', null=True, blank=True)
    precio_cliente = models.CharField(max_length=50, null=True, blank=True)
    precio_prov = models.CharField(max_length=50, null=True, blank=True)
    categoria_viaje = models.ForeignKey(CategoriaViaje, null=True, blank=True)
    tarifario = models.ForeignKey(Tarifario, null=True, blank=True)
    baja = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.descripcion

    def __str__(self):
        return self.descripcion

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
    if aaaammddhhmm == None:
        return ""
    return aaaammddhhmm[8:10] + ":" + aaaammddhhmm[10:12] + " " + aaaammddhhmm[6:8] + "/" + aaaammddhhmm[4:6] + "/" + aaaammddhhmm[0:4]

def getFecha(aaaammdd):
    if aaaammdd == None:
        return ""
    return aaaammdd[6:8] + "/" + aaaammdd[4:6] + "/" + aaaammdd[0:4]

class TipoAdelanto (models.Model):
    descripcion= models.CharField(max_length=50, null=True, blank=True)
    logica= models.CharField(max_length=50, null=True, blank=True)
    

    def __unicode__(self):
        return u'%s' % self.descripcion

    def __str__(self):
        return self.descripcion
		
class Adelanto (models.Model):
    persona_id = models.ForeignKey(Persona, null=True, blank=True)
    tipo_adelanto_id = models.ForeignKey(TipoAdelanto, null=True, blank=True)
    fecha = models.CharField(max_length=20, null=True, blank=True)
    monto = models.CharField(max_length=25, null=True, blank=True)
    Factura_id= models.CharField(max_length=25, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.persona_id

    def __str__(self):
        return self.persona_id