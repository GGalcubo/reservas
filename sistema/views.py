# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.template.defaulttags import register
from django.conf import settings
from .models import *
from django.http import HttpResponse
from django.core import serializers
import json
import os

@login_required
def dashboard(request):
    mensaje = ""
    context = { 'mensaje':mensaje }
    return render(request, 'sistema/dashboard.html', context)

@login_required
def operaciones(request):
    mensaje = ""

    viajes = Viaje.objects.all()
    clientes = Cliente.objects.all()
    unidades = Unidad.objects.all()
    estados = Estado.objects.all()
    categoria_viajes = CategoriaViaje.objects.all()

    context = {'mensaje': mensaje, 'estados': estados,'categoria_viajes': categoria_viajes}
    return render(request, 'sistema/operaciones.html', context)

@login_required
def asignaciones(request):
    mensaje = ""

    viajes = Viaje.objects.all()
    unidades = Unidad.objects.all()
    estados = Estado.objects.all()

    context = {'mensaje':mensaje, 'viajes': viajes, 'unidades': unidades, 'estados': estados, }
    return render(request, 'sistema/asignaciones.html', context)

@login_required
def getViajesAsignacionesPorFecha(request):
    mensaje = ""
    date = getAAAAMMDD(request.POST.get('date', False))

    estados_get_seleccionados = request.POST.getlist('estados_selecionados[]', False)
    estados_seleccionados = []
    if estados_get_seleccionados == False:
        estados_seleccionados = [1, 2, 4]
    else:
        for i in estados_get_seleccionados:
            estados_seleccionados.append(i)

    viajes = Viaje.objects.filter(fecha=date).filter(estado__in=estados_seleccionados)
    context = {'mensaje': mensaje, 'viajes': viajes}
    return render(request, 'sistema/grillaViajesAsignaciones.html', context)

@login_required
def altaViaje(request):
    mensaje     = ""
    es_nuevo    = 1
    viaje       = Viaje()
    viaje.id    = 0

    context = {'mensaje': mensaje,
               'clientes':Cliente.objects.all(),
               'tipoobservacion':TipoObservacion.objects.all(),
               #'observacion':Observacion.objects.all(),
               'tipo_pago':TipoPagoViaje.objects.all(),
               'unidades':Unidad.objects.all(),
               'estados':Estado.objects.all(),
               'categoria_viajes':CategoriaViaje.objects.all(),
               'destinos':TrayectoDestino.objects.all(),
               'localidades':CategoriaViaje.objects.all(),
               'provincias':Provincia.objects.all(),
               'es_nuevo':es_nuevo,
               'viaje':viaje}

    return render(request, 'sistema/viaje.html', context)

@login_required
def editaViaje(request):
    mensaje     = ""
    es_nuevo    = 0
    id_viaje    = request.GET.get('idViaje', "")
    if request.GET.get('msg', "") == '1':
        mensaje = 'El viaje se creo correctamente.'
    viaje = Viaje.objects.get(id=id_viaje)
    # used to generate random unique id
    #import uuid #uid = uuid.uuid4()

    context = {'mensaje': mensaje,
               'clientes':Cliente.objects.all(),
               #'uid':uuid.uuid4(),
               'tipoobservacion':TipoObservacion.objects.all(),
               #'observaciones':Observacion.objects.all(),
               'tipo_pago':TipoPagoViaje.objects.all(),
               'itemsviaje':ItemViaje.objects.filter(viaje_id=id_viaje),
               'unidades':Unidad.objects.all(),
               'estados':Estado.objects.all(),
               'categoria_viajes':CategoriaViaje.objects.all(),
               'destinos':TrayectoDestino.objects.all(),
               'localidades':Localidad.objects.all(),
               'provincias':Provincia.objects.all(),
               'es_nuevo':es_nuevo,
               'viaje':viaje,
               'trayectos':Trayecto.objects.filter(viaje_id=id_viaje)}
    return render(request, 'sistema/viaje.html', context)


@login_required
def guardarViaje(request):

    es_nuevo = request.POST.get('es_nuevo', "1")
    mensaje = ''

    if es_nuevo == "1":
        viaje = Viaje()
    else:
        viaje = Viaje.objects.get(id=request.POST.get('idViaje', False))
        mensaje = 'El viaje se actualizo correctamente.'

    viaje.estado 				= Estado.objects.get(id=request.POST.get('estado', False))
    viaje.cliente 				= Cliente.objects.get(id=request.POST.get('cliente', False))
    viaje.categoria_viaje 		= CategoriaViaje.objects.get(id=request.POST.get('categoria_viaje', False))
    viaje.solicitante 			= Persona.objects.get(id=request.POST.get('contacto', False))
    viaje.centro_costo 			= CentroCosto.objects.get(id=request.POST.get('centro_costos', False))
    pasajero                    = Persona.objects.get(id=request.POST.get('pasajero', False))
    viaje.pasajero 				= pasajero
    fecha_tmp 					= request.POST.get('fecha', "")
    viaje.fecha 				= fecha_tmp[6:10] + fecha_tmp[3:5] + fecha_tmp[0:2]
    viaje.hora 					= request.POST.get('hora', "")
    viaje.hora_estimada 		= request.POST.get('hora_estimada', "")
    viaje.tarifapasada 			= request.POST.get('tarifa_pasada', "")
    viaje.Cod_ext_viaje         = request.POST.get('cod_externo', "")
    viaje.nro_aux               = request.POST.get('nro_aux', "")
    viaje.tipo_pago             = TipoPagoViaje.objects.get(id=request.POST.get('tipo_pago', False))
    unidad 						= request.POST.get('unidad', '')
    if unidad != '':
        viaje.unidad 			= Unidad.objects.get(id=unidad)


    data = {
        'error': '0',
        'msg': mensaje
    }

    viaje.save()

    #guardaViajePasajero(pasajero, True, viaje)
    guardaItemViaje(request.POST.get('importe_efectivo', ''), 12, 1, viaje, False)
    guardaItemViaje(request.POST.get('otros', ''), 16, 1, viaje, False)
    guardaItemViaje(request.POST.get('peaje', ''), 15, 1, viaje, False)
    guardaItemViaje(request.POST.get('estacionamiento', ''), 11, 1, viaje, False)
    guardaObsViaje(request.POST.get('comentario_chofer', ''), viaje, request)

    if viaje.estado.id == 6 or viaje.estado.id == 7:
        guardaItemViajeCostoProveedor('', 8, 1, viaje, False)
        guardaItemViajeHsDispo       ('', 13, request.POST.get('tiempo_hs_dispo', ''), viaje, False)
        guardaItemViajeEspera        ('', 14, request.POST.get('tiempo_espera', ''), viaje, False)
        guardaItemViajeBilingue      ('', 9, request.POST.get('bilingue', ''), viaje, False)
        guardaItemViajeMaletas       ('', 10, request.POST.get('maletas', ''), viaje, False)


        guardaItemViaje              (request.POST.get('otros', ''), 17, 1, viaje, False)
        guardaItemViaje              (request.POST.get('peaje', ''), 6, 1, viaje, False)
        guardaItemViaje              (request.POST.get('estacionamiento', ''), 5, 1, viaje, False)
        guardaItemViajeCostoCliente  ('', 2, 1, viaje, False)
        guardaItemViajeHsDispoAdmin  ('', 18, request.POST.get('tiempo_hs_dispo', ''), viaje, False)
        guardaItemViajeEsperaAdmin   ('', 1, request.POST.get('tiempo_espera', ''), viaje, False)
        guardaItemViajeBilingueAdmin ('', 3, request.POST.get('bilingue', ''), viaje, False)
        guardaItemViajeMaletasAdmin  ('', 4, request.POST.get('maletas', ''), viaje, False)

        items_viaje = serializers.serialize('json',ItemViaje.objects.filter(viaje=viaje))
        return HttpResponse(items_viaje, content_type='application/json')

    if es_nuevo == "1":
        data = {
            'url': '/sistema/editaViaje/?idViaje=' + str(viaje.id) + '&msg=1',
        }

    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

def guardaViajeAdmin(request):
    viaje = Viaje.objects.get(id=request.POST.get('viaje', False))

    guardaItemViaje(request.POST.get('admin_otros_proveedor', ''), 16, 1, viaje, True)
    guardaItemViaje(request.POST.get('admin_peaje_proveedor', ''), 15, 1, viaje, True)
    guardaItemViaje(request.POST.get('admin_estacionamiento_proveedor', ''), 11, 1, viaje, True)
    guardaItemViajeCostoProveedor(request.POST.get('admin_costo_proveedor', ''), 8, 1, viaje, True)
    guardaItemViajeHsDispo(request.POST.get('admin_hs_dispo_proveedor', ''), 18, request.POST.get('tiempo_hs_dispo', ''), viaje, True)
    guardaItemViajeEspera(request.POST.get('admin_espera_proveedor', ''), 14, request.POST.get('tiempo_espera', ''), viaje, True)
    guardaItemViajeBilingue(request.POST.get('admin_costo_bilingue_proveedor', ''), 3, request.POST.get('bilingue', ''), viaje, True)
    guardaItemViajeMaletas(request.POST.get('admin_costo_maletas_proveedor', ''), 4, request.POST.get('maletas', ''), viaje, True)

    guardaItemViaje(request.POST.get('admin_otros_cliente', ''), 17, 1, viaje, True)
    guardaItemViaje(request.POST.get('admin_peaje_cliente', ''), 6, 1, viaje, True)
    guardaItemViaje(request.POST.get('admin_estacionamiento_cliente', ''), 5, 1, viaje, True)
    guardaItemViajeCostoCliente(request.POST.get('admin_costo_cliente', ''), 2, 1, viaje, True)
    guardaItemViajeHsDispoAdmin(request.POST.get('admin_hs_dispo_cliente', ''), 18, request.POST.get('tiempo_hs_dispo', ''), viaje, True)
    guardaItemViajeEsperaAdmin(request.POST.get('admin_espera_cliente', ''), 1, request.POST.get('tiempo_espera', ''), viaje, True)
    guardaItemViajeBilingueAdmin(request.POST.get('admin_costo_bilingue_cliente', ''), 3, request.POST.get('bilingue', ''), viaje, True)
    guardaItemViajeMaletasAdmin(request.POST.get('admin_costo_maletas_cliente', ''), 4, request.POST.get('maletas', ''), viaje, True)

    items_viaje = serializers.serialize('json', ItemViaje.objects.filter(viaje=viaje))
    return HttpResponse(items_viaje, content_type='application/json')

def guardaItemViajeCostoProveedor(monto, tipo_item_viaje, cant, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        trayecto = viaje.getTrayectoPrincipal()
        tarifa_viaje = TarifaViaje.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, localidad_desde=trayecto.localidad_desde, localidad_hasta=trayecto.localidad_hasta)
        base = tarifa_viaje.precio_prov
    except Exception as e:
        base = 0
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
    except ItemViaje.DoesNotExist:
        monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(base), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = cant
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeCostoCliente(monto, tipo_item_viaje, cant, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    monto_s_iva     = 0
    monto_iva       = 0
    try:
        trayecto = viaje.getTrayectoPrincipal()
        tarifa_viaje = TarifaViaje.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, localidad_desde=trayecto.localidad_desde, localidad_hasta=trayecto.localidad_hasta)
        base = tarifa_viaje.precio_cliente
    except Exception as e:
        base = 0
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
    except ItemViaje.DoesNotExist:
        monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(base), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = cant
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeMaletas(monto, tipo_item_viaje, checkbox, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='maletas')
    monto_s_iva     = 0
    monto_iva       = 0
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        checkbox = 1 if checkbox == 'on' else 0
    except ItemViaje.DoesNotExist:
        if checkbox == '' and monto == '':
            return
        else:
            checkbox = 1 if checkbox == 'on' else 0
            monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(tarifa_extra.extra_precio_prov), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = checkbox
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeMaletasAdmin(monto, tipo_item_viaje, checkbox, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='maletas')
    monto_s_iva     = 0
    monto_iva       = 0
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        checkbox = 1 if checkbox == 'on' else 0
    except ItemViaje.DoesNotExist:
        if checkbox == '' and monto == '':
            return
        else:
            checkbox = 1 if checkbox == 'on' else 0
            monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(tarifa_extra.extra_precio), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = checkbox
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeBilingue(monto, tipo_item_viaje, checkbox, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        trayecto = viaje.getTrayectoPrincipal()
        tarifa_viaje = TarifaViaje.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, localidad_desde=trayecto.localidad_desde, localidad_hasta=trayecto.localidad_hasta)
        base = tarifa_viaje.precio_prov
    except Exception as e:
        base = 0

    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        checkbox = 1 if checkbox == 'on' else 0
    except ItemViaje.DoesNotExist:
        if checkbox == '' and monto == '':
            return
        else:
            checkbox = 1 if checkbox == 'on' else 0
            monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(base) * 0.2, 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = checkbox
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeBilingueAdmin(monto, tipo_item_viaje, checkbox, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        trayecto = viaje.getTrayectoPrincipal()
        tarifa_viaje = TarifaViaje.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, localidad_desde=trayecto.localidad_desde, localidad_hasta=trayecto.localidad_hasta)
        base = tarifa_viaje.precio_cliente
    except Exception as e:
        base = 0

    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        checkbox = 1 if checkbox == 'on' else 0
    except ItemViaje.DoesNotExist:
        if checkbox == '' and monto == '':
            return
        else:
            checkbox = 1 if checkbox == 'on' else 0
            monto = 0 if monto == '' else monto
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round(float(base) * 0.2, 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = checkbox
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeEspera(monto, tipo_item_viaje, tiempo, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='espera')
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        tiempo = 0 if tiempo == '' else tiempo
    except ItemViaje.DoesNotExist:
        if tiempo == '' and monto == '':
            return
        else:
            monto = 0 if monto == '' else monto
            tiempo = 0 if tiempo == '' else tiempo
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round((int(tiempo)/15) * float(tarifa_extra.extra_precio_prov), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = tiempo
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeEsperaAdmin(monto, tipo_item_viaje, tiempo, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='espera')
    monto_s_iva     = 0
    monto_iva       = 0
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        tiempo = 0 if tiempo == '' else tiempo
    except ItemViaje.DoesNotExist:
        if tiempo == '' and monto == '':
            return
        else:
            monto = 0 if monto == '' else monto
            tiempo = 0 if tiempo == '' else tiempo
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else round((int(tiempo)/15) * float(tarifa_extra.extra_precio), 2)
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = tiempo
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeHsDispo(monto, tipo_item_viaje, tiempo, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='dispo')
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        tiempo = 0 if tiempo == '' else tiempo
    except ItemViaje.DoesNotExist:
        if monto == '' and tiempo == '':
            return
        else:
            monto = 0 if monto == '' else monto
            tiempo = 0 if tiempo == '' else tiempo
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else int(tiempo) * round(float(tarifa_extra.extra_precio_prov))
    monto_iva   = round(monto_s_iva * tipo_item_viaje.iva_pct, 2) if manual else round(monto_s_iva * tipo_item_viaje.iva_pct, 2)

    item_viaje_otros.cant               = tiempo
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViajeHsDispoAdmin(monto, tipo_item_viaje, tiempo, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    centro_costo    = viaje.centro_costo
    tarifa_extra    = TarifaExtra.objects.get(categoria_viaje=viaje.categoria_viaje, tarifario=centro_costo.tarifario, extra_descripcion='dispo')
    monto_s_iva     = 0
    monto_iva       = 0

    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
        tiempo = 0 if tiempo == '' else tiempo
    except ItemViaje.DoesNotExist:
        if monto == '' and tiempo == '':
            return
        else:
            monto = 0 if monto == '' else monto
            tiempo = 0 if tiempo == '' else tiempo
        item_viaje_otros = ItemViaje()

    monto       = round(float(monto), 2)
    monto_s_iva = monto if manual else int(tiempo) * round(float(tarifa_extra.extra_precio), 2)
    monto_iva   = monto_s_iva * tipo_item_viaje.iva_pct if manual else monto_s_iva * tipo_item_viaje.iva_pct

    item_viaje_otros.cant               = tiempo
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto_s_iva
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto_iva
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaItemViaje(monto, tipo_item_viaje, cant, viaje, manual):
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        monto = 0 if monto == '' else monto
    except ItemViaje.DoesNotExist:
        if monto == '':
            return
        item_viaje_otros = ItemViaje()

    monto                               = round(float(monto), 2)
    item_viaje_otros.cant               = cant
    item_viaje_otros.monto              = monto
    item_viaje_otros.monto_s_iva        = monto
    item_viaje_otros.viaje              = viaje

    item_viaje_otros.monto_iva          = monto * tipo_item_viaje.iva_pct
    item_viaje_otros.tipo_items_viaje   = tipo_item_viaje
    item_viaje_otros.save()

def guardaViajePasajeroPOST(request):
    viaje                        = Viaje.objects.get(id=request.POST.get('viaje', False))
    viaje_pasajero               = ViajePasajero()
    viaje_pasajero.viaje         = viaje
    viaje_pasajero.pasajero      = Persona.objects.get(id=request.POST.get('pasajero', False))
    viaje_pasajero.pasajero_ppal = False
    viaje_pasajero.save()

    context = {'viaje':viaje}
    return render(request, 'sistema/grillaPasajerosViaje.html', context)

def getViajePasajeros(request):
    viaje = Viaje.objects.get(id=request.POST.get('viaje', False))

    dump = serializers.serialize('json', viaje.getPasajeros())
    return HttpResponse(dump, content_type='application/json')

def deleteViajePasajero(request):
    viaje = Viaje.objects.get(id=request.POST.get('viaje', False))
    ViajePasajero.objects.filter(pasajero_id=request.POST.get('pasajero', False), viaje=viaje).delete()

    context = {'viaje':viaje}
    return render(request, 'sistema/grillaPasajerosViaje.html', context)

def deleteAllViajePasajero(request):
    viaje = Viaje.objects.get(id=request.POST.get('viaje', False))
    ViajePasajero.objects.filter(viaje=viaje).delete()

    context = {'viaje':viaje}
    return render(request, 'sistema/grillaPasajerosViaje.html', context)

def guardaViajePasajero(pasajero, principal, viaje):
    try:
        viaje_pasajero = ViajePasajero.objects.get(viaje=viaje, pasajero_ppal=principal)
    except ViajePasajero.DoesNotExist:
        viaje_pasajero = ViajePasajero()

    viaje_pasajero.viaje         = viaje
    viaje_pasajero.pasajero      = pasajero
    viaje_pasajero.pasajero_ppal = principal
    viaje_pasajero.save()

def guardaObsViaje(input_text, viaje, request):

    if len(viaje.observacionviaje_set.all()) > 0:
        observacion = viaje.observacionviaje_set.all()[0].observacion
        ob_viaje = viaje.observacionviaje_set.all()[0]
    else:
        if input_text == '':
            return
        ob_viaje = ObservacionViaje()
        observacion = Observacion()
        observacion.tipo_observacion = TipoObservacion.objects.get(id=17)

    observacion.fecha = fecha()
    observacion.usuario = request.user
    observacion.texto = input_text
    observacion.save()

    ob_viaje.viaje = viaje
    ob_viaje.observacion = observacion
    ob_viaje.save()

@login_required
def guardarViajeAdjunto(request):
    idViaje = request.POST["idViaje"]
    viaje   = Viaje.objects.get(id=idViaje)
    file    = request.FILES['file']
    error   = False

    options = {
        "maxfilesize": 2 * 2 ** 20,  # 2 Mb
        "minfilesize": 1 * 2 ** 10,  # 1 Kb
        "acceptedformats": (
            "image/jpeg",
            "image/png",
            "application/pdf",
            "application/msword",
        )
    }
    # file size
    if file.size > options["maxfilesize"]:
        error = "maxFileSize"
    if file.size < options["minfilesize"]:
        error = "minFileSize"
        # allowed file type
    #if file.content_type not in options["acceptedformats"]:
        #error = "acceptFileTypes"

    response_data = {
        "name": file.name,
        "size": file.size,
        "type": file.content_type
    }

    if error:
        response_data["error"] = error
        response_data = json.dumps([response_data])
        return HttpResponse(response_data, mimetype='application/json')

    adjunto = Adjunto()
    adjunto.upload = request.FILES['file']
    adjunto.fecha = '2018'
    adjunto.save()

    viajeAdjunto = AdjuntoViaje()
    viajeAdjunto.adjunto = adjunto
    viajeAdjunto.viaje_id = idViaje
    viajeAdjunto.save()

    context = {'viaje': viaje}
    return render(request, 'sistema/grillaAdjuntos.html', context)

def deleteViajeAdjunto(request):
    viaje = Viaje.objects.get(id=request.POST.get('viaje', False))
    AdjuntoViaje.objects.filter(adjunto_id=request.POST.get('adjunto_id', False), viaje=viaje).delete()

    context = {'viaje': viaje}
    return render(request, 'sistema/grillaAdjuntos.html', context)

@login_required
def guardarTrayecto(request):

    trayectos = Trayecto.objects.filter(viaje_id=request.POST.get('idViaje', False))
    principal = request.POST.get('principal', '')

    if principal != '1' and trayectos.count() == 0:
        data = {
            'error': '1',
            'msg': 'Debes crear un trayecto principal antes de agregar trayectos secundarios.'
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    else:
        viaje = Viaje.objects.get(id=request.POST.get('idViaje', False))

        if trayectos.count() == 0 and principal == '1':
            trayecto = Trayecto()
        elif trayectos.count() >= 1 and principal == '1':
            trayecto = viaje.getTrayectoPrincipal()
        else:
            id = request.POST.get('id', '')
            if id == '0':
                trayecto = Trayecto()
            else:
				trayecto = Trayecto.objects.get(id=id)


        trayecto.viaje = viaje
        trayecto.destino_desde = TrayectoDestino.objects.get(id=request.POST.get('desde_destino', False))
        if request.POST.get('desde_localidad', '') != '':
            trayecto.localidad_desde = Localidad.objects.get(id=request.POST.get('desde_localidad', False))
        if request.POST.get('desde_provincia', '') != '':
            trayecto.provincia_desde = Provincia.objects.get(id=request.POST.get('desde_provincia', False))
        trayecto.altura_desde = request.POST.get('desde_altura', '')
        trayecto.calle_desde = request.POST.get('desde_calle', '')
        trayecto.entre_desde = request.POST.get('desde_entre', '')
        trayecto.compania_desde = request.POST.get('desde_compania', '')
        trayecto.vuelo_desde = request.POST.get('desde_vuelo', '')
        trayecto.destino_hasta = TrayectoDestino.objects.get(id=request.POST.get('hasta_destino', False))
        if request.POST.get('hasta_localidad', '') != '':
            trayecto.localidad_hasta = Localidad.objects.get(id=request.POST.get('hasta_localidad', False))
        if request.POST.get('hasta_provincia', '') != '':
            trayecto.provincia_hasta = Provincia.objects.get(id=request.POST.get('hasta_provincia', False))
        trayecto.altura_hasta = request.POST.get('hasta_altura', '')
        trayecto.calle_hasta = request.POST.get('hasta_calle', '')
        trayecto.entre_hasta = request.POST.get('hasta_entre', '')
        trayecto.compania_hasta = request.POST.get('hasta_compania', '')
        trayecto.vuelo_hasta = request.POST.get('hasta_vuelo', '')
        trayecto.save()

        if principal == '1':
            data = {
                'error': '0',
                'msg': 'Los datos han sido guardados correctamente.'
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')
        else:
            mensaje = ''
            context = {'mensaje': mensaje, 'trayectos': trayectos}
            return render(request, 'sistema/grillaTramos.html', context)

@login_required
def borrarTrayecto(request):
    id = request.POST.get('id', '')
    trayecto = Trayecto.objects.get(id=id)
    trayecto.delete()

    trayectos = Trayecto.objects.filter(viaje_id=request.POST.get('idViaje', False))
    mensaje = ''
    context = {'mensaje': mensaje, 'trayectos': trayectos}
    return render(request, 'sistema/grillaTramos.html', context)

@login_required
def guardarSolicitanteDesdeViaje(request):
    mensaje = ""
    idClienteEnSol = request.POST.get('idClienteEnSol', "")
    cliente = Cliente.objects.get(id=idClienteEnSol)
    idSol = request.POST.get('idSolicitante', "")
    if idSol == "0":
        persona = Persona()
        persona.tipo_persona = TipoPersona.objects.get(id=1)
    else:
        persona = Persona.objects.get(id=idSol)

    persona.nombre = request.POST.get('nombrePasajeroCliente', "")
    persona.apellido = request.POST.get('apellidoPasajeroCliente', "")
    persona.puesto = request.POST.get('puestoSol', "")
    persona.mail = request.POST.get('mailSol', "")
    persona.save()
    telefono = request.POST.get('telefonoSol', "")

    if idSol == "0":
        perCli = PersonaCliente()
        perCli.persona = persona
        perCli.cliente = cliente
        perCli.save()

    if telefono != "" and telefono != "Sin telefono":
        if len(persona.telefonopersona_set.all()) > 0:
            tel = persona.telefonopersona_set.all()[0].telefono
            telcli = persona.telefonopersona_set.all()[0]
        else:
            telcli = TelefonoPersona()
            tel = Telefono()
            tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")

        tel.numero = telefono
        tel.save()

        telcli.persona = persona
        telcli.telefono = tel
        telcli.save()

    context = {'mensaje': mensaje, 'cliente':cliente}
    return render(request, 'sistema/selectSolicitante.html', context)

@login_required
def guardarPasajeroDesdeViaje(request):
    mensaje = ""
    idClientePasajero = request.POST.get('idClientePasajeroModal', "")
    print idClientePasajero
    cliente = Cliente.objects.get(id=idClientePasajero)
    idPasajero = request.POST.get('idPasajeroModal', "")
    if idPasajero == "0":
        persona = Persona()
        persona.tipo_persona = TipoPersona.objects.get(id=2)
    else:
        persona = Persona.objects.get(id=idPasajero)

    persona.nombre = request.POST.get('nombrePasClienteModal', "")
    persona.apellido = request.POST.get('apellidoPasClienteModal', "")
    persona.documento = request.POST.get('documentoPasajeroClienteModal', "")
    persona.mail = request.POST.get('mailPasajeroClienteModal', "")
    persona.nacionalidad = request.POST.get('nacionalidadPasajeroClienteModal', "")
    persona.calle = request.POST.get('callePasajeroClienteModal', "")
    #persona.altura = request.POST.get('alturaPasajeroCliente', "")
    #persona.piso = request.POST.get('pisoPasajeroCliente', "")
    #persona.cp = request.POST.get('cpPasajeroCliente', "")
    persona.save()

    telefono = request.POST.get('telefonoPasajeroClienteModal', "")
    comentario = request.POST.get('comentarioPasajeroClienteModal', "")

    if idPasajero == "0":
        perCli = PersonaCliente()
        perCli.persona = persona
        perCli.cliente = cliente
        perCli.save()

    if telefono != "" and telefono != "Sin telefono":
        if len(persona.telefonopersona_set.all()) > 0:
            tel = persona.telefonopersona_set.all()[0].telefono
            telcli = persona.telefonopersona_set.all()[0]
        else:
            telcli = TelefonoPersona()
            tel = Telefono()
            tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")

        tel.numero = telefono
        tel.save()

        telcli.persona = persona
        telcli.telefono = tel
        telcli.save()

    if comentario != "":
        if len(persona.observacionpersona_set.all()) > 0:
            obs = persona.observacionpersona_set.all()[0].observacion
            obsper = persona.observacionpersona_set.all()[0]
        else:
            obsper = ObservacionPersona()
            obs = Observacion()
            obs.tipo_observacion = TipoObservacion.objects.get(id=16)

        obs.fecha = fecha()
        obs.usuario = request.user
        obs.texto = comentario
        obs.save()

        obsper.persona = persona
        obsper.observacion = obs
        obsper.save()

    context = {'mensaje': mensaje, 'cliente':cliente}
    return render(request, 'sistema/selectPasajero.html', context)


@login_required
def altaPersona(request):
	mensaje = ""
	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaPersona.html', context)

@login_required
def editaPersona(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaPersona.html', context)

@login_required
def guardarOwnerProspect(request):
	persona = Persona()
	persona.nombre = request.POST.get('nombreDuenio', "")
	persona.apellido = request.POST.get('apellidoDuenio', "")
	persona.tipo_persona_id = 4
	persona.save()

	telefono = request.POST.get('telefonoDuenio', "")
	if telefono != "":
		tel = Telefono()
		tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")
		tel.numero = telefono
		tel.save()

		telcli = TelefonoPersona()
		telcli.persona = persona
		telcli.telefono = tel
		telcli.save()

	data = {
		'persona_id': persona.id,
		'persona_nombre': persona.nombre,
		'persona_apellido':persona.apellido
	}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

def guardarChoferProspect(request):
	persona = Persona()
	persona.nombre = request.POST.get('nombreChofer', "")
	persona.apellido = request.POST.get('apellidoChofer', "")
	persona.porcentaje_viaje = request.POST.get('porcentajeChofer', "")
	persona.tipo_persona_id = 3
	persona.save()

	telefono = request.POST.get('telefonoChofer', "")
	if telefono != "":
		tel = Telefono()
		tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")
		tel.numero = telefono
		tel.save()

		telcli = TelefonoPersona()
		telcli.persona = persona
		telcli.telefono = tel
		telcli.save()

	data = {
		'persona_id': persona.id,
		'persona_nombre': persona.nombre,
		'persona_apellido':persona.apellido,
		'persona_porcentaje':persona.porcentaje_viaje
	}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def guardarCentroCostoProspect(request):
	mensaje = ""
	trayectos = ""
	idCC = request.POST.get('idClienteCC', "")
	if idCC == "0":
		cc = CentroCosto()
		cliente = Cliente.objects.get(id=request.POST.get('idClienteEnCC', ""))
		cc.cliente = cliente
	else:
		cc = CentroCosto.objects.get(id=idCC)
		cliente = cc.cliente

	cc.nombre = request.POST.get('codigoCCCliente', "")
	cc.fecha_inicio = getAAAAMMDD(request.POST.get('desdeCC', ""))
	cc.fecha_fin = getAAAAMMDD(request.POST.get('hastaCC', ""))
	cc.descripcion = request.POST.get('descripcionCCCliente', "")
	cc.tarifario = Tarifario.objects.get(id=request.POST.get('selectTarifariosCCCliente', ""))
	cc.save()

	context = {'mensaje': mensaje, 'trayectos': trayectos, 'cliente':cliente}
	return render(request, 'sistema/grillaCentroCostos.html', context)



@login_required
def guardarSolicitanteProspect(request):
	mensaje = ""
	idClienteEnSol = request.POST.get('idClienteEnSol', "")
	cliente = Cliente.objects.get(id=idClienteEnSol)
	idSol = request.POST.get('idSolicitante', "")
	if idSol == "0":
		persona = Persona()
		persona.tipo_persona = TipoPersona.objects.get(id=1)
	else:
		persona = Persona.objects.get(id=idSol)

	persona.nombre = request.POST.get('nombrePasajeroCliente', "")
	persona.apellido = request.POST.get('apellidoPasajeroCliente', "")
	persona.puesto = request.POST.get('puestoSol', "")
	persona.mail = request.POST.get('mailSol', "")
	persona.save()
	telefono = request.POST.get('telefonoSol', "")

	if idSol == "0":
		perCli = PersonaCliente()
		perCli.persona = persona
		perCli.cliente = cliente
		perCli.save()
	
	if telefono != "" and telefono != "Sin telefono":
		if len(persona.telefonopersona_set.all()) > 0:
			tel = persona.telefonopersona_set.all()[0].telefono
			telcli = persona.telefonopersona_set.all()[0]
		else:
			telcli = TelefonoPersona()
			tel = Telefono()
			tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")

		tel.numero = telefono
		tel.save()

		telcli.persona = persona
		telcli.telefono = tel
		telcli.save()

	context = {'mensaje': mensaje, 'cliente':cliente}
	return render(request, 'sistema/grillaSolicitantes.html', context)

@login_required
def guardarPasajeroProspect(request):
    mensaje = ""
    idClientePasajero = request.POST.get('idClientePasajero', "")
    print idClientePasajero
    cliente = Cliente.objects.get(id=idClientePasajero)
    idPasajero = request.POST.get('idPasajero', "")
    if idPasajero == "0":
		persona = Persona()
		persona.tipo_persona = TipoPersona.objects.get(id=2)
    else:
		persona = Persona.objects.get(id=idPasajero)

    persona.nombre = request.POST.get('nombrePasCliente', "")
    persona.apellido = request.POST.get('apellidoPasCliente', "")
    persona.documento = request.POST.get('documentoPasajeroCliente', "")
    persona.mail = request.POST.get('mailPasajeroCliente', "")
    persona.nacionalidad = request.POST.get('nacionalidadPasajeroCliente', "")
    persona.calle = request.POST.get('callePasajeroCliente', "")
    #persona.altura = request.POST.get('alturaPasajeroCliente', "")
    #persona.piso = request.POST.get('pisoPasajeroCliente', "")
    #persona.cp = request.POST.get('cpPasajeroCliente', "")
    persona.save()

    telefono = request.POST.get('telefonoPasajeroCliente', "")
    comentario = request.POST.get('comentarioPasajeroCliente', "")

    if idPasajero == "0":
		perCli = PersonaCliente()
		perCli.persona = persona
		perCli.cliente = cliente
		perCli.save()

    if telefono != "" and telefono != "Sin telefono":
		if len(persona.telefonopersona_set.all()) > 0:
			tel = persona.telefonopersona_set.all()[0].telefono
			telcli = persona.telefonopersona_set.all()[0]
		else:
			telcli = TelefonoPersona()
			tel = Telefono()
			tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")

		tel.numero = telefono
		tel.save()

		telcli.persona = persona
		telcli.telefono = tel
		telcli.save()

    if comentario != "":
        if len(persona.observacionpersona_set.all()) > 0:
            obs = persona.observacionpersona_set.all()[0].observacion
            obsper = persona.observacionpersona_set.all()[0]
        else:
            obsper = ObservacionPersona()
            obs = Observacion()
            obs.tipo_observacion = TipoObservacion.objects.get(id=16)

        obs.fecha = fecha()
        obs.usuario = request.user
        obs.texto = comentario
        obs.save()

        obsper.persona = persona
        obsper.observacion = obs
        obsper.save()

	context = {'mensaje': mensaje, 'cliente':cliente}
	return render(request, 'sistema/grillaPasajeros.html', context)

@login_required
def listadoCliente(request, **kwargs):
	clientes = Cliente.objects.filter(baja=False)
	context = {'clientes': clientes}
	return render(request, 'sistema/listadoCliente.html', context)

@login_required
def cliente(request):
	mensaje = ""
	idCliente = request.GET.get('idCliente', "")
	cliente = Cliente.objects.get(id=idCliente)
	tarifarios = Tarifario.objects.all()
	ivas = Iva.objects.all()
	condiciones = CondicionPago.objects.all()
	context = {'mensaje': mensaje, 'cliente':cliente, 'tarifarios':tarifarios,"ivas":ivas, "condiciones": condiciones }
	return render(request, 'sistema/cliente.html', context)

@login_required
def altaCliente(request):
	mensaje = ""
	cliente = Cliente()
	cliente.id = 0
	tarifarios = Tarifario.objects.all()
	context = {'mensaje': mensaje, 'tarifarios':tarifarios, 'cliente': cliente }
	return render(request, 'sistema/cliente.html', context)

@login_required
def guardarCliente(request):
	idCliente = request.POST.get('idCliente', "")
	if idCliente == "0":
		cliente = Cliente()
		tel = Telefono()
	else:
		cliente = Cliente.objects.get(id=idCliente)
		if len(cliente.telefonocliente_set.all()) > 0:
			tel = cliente.telefonocliente_set.all()[0].telefono
		else:
			tel = Telefono()
		
	cliente.razon_social = request.POST.get('razonSocial', "")
	cliente.cuil = request.POST.get('cuil', "")
	cliente.calle = request.POST.get('calle', "")
	cliente.altura = request.POST.get('altura',"")
	cliente.piso = request.POST.get('piso', "")
	cliente.depto = request.POST.get('depto', "")
	cliente.cp = request.POST.get('cp', "")
	cliente.localidad = request.POST.get('localidad', "")
	cliente.provincia = request.POST.get('provincia', "")
	iva = request.POST.get('iva', "")
	if iva != "":
		cliente.iva = Iva.objects.get(id=iva)
	cond = request.POST.get('condicionPago', "")
	if cond != "":
		cliente.condicion_pago = CondicionPago.objects.get(id=cond)
	cliente.dias_fechas_facturas = request.POST.get('diasFechaFactura', "")
	cliente.alias = request.POST.get('alias', "")
	cliente.cbu = request.POST.get('cbu', "")

	cliente.save()

	if request.POST.get('telefono', False) != "":
		tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")
		tel.numero = request.POST.get('telefono', False)
		tel.save()

		if idCliente == "0":
			telcli = TelefonoCliente()
			telcli.cliente = cliente
			telcli.telefono = tel
			telcli.save()

	url = '/sistema/cliente/?idCliente='+str(cliente.id)
	return redirect(url)

@login_required
def editaCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/cliente.html', context)

@login_required
def eliminarCliente(request):
	idCliente = request.POST.get('idClienteEliminar', False)
	cliente = Cliente.objects.get(id=idCliente)
	cliente.baja = True
	cliente.save()

	return redirect('listadoCliente')


@login_required
def guardarObservacionViaje(request):
	mensaje = ""

	idViaje = request.POST.get('idViajeObser', False)
	text_obs = request.POST.get('text_obs', False)
	#hora_obs = request.POST.get('hora_obs', fecha())
	detalle_obs = request.POST.get('detalle_obs', False)
	observacion = Observacion()
	observacion.fecha = fecha()
	observacion.usuario = request.user
	observacion.texto = text_obs
	observacion.tipo_observacion = TipoObservacion.objects.get(id=detalle_obs)
	observacion.save()

	viaje = Viaje.objects.get(id=idViaje)

	obcl = ObservacionViaje()
	obcl.observacion = observacion
	obcl.viaje = viaje
	obcl.save()

	context = {'mensaje': mensaje, 'viaje':viaje}
	return render(request, 'sistema/grillaObservacionesViaje.html', context)


@login_required
def guardarObservacionCliente(request):
	mensaje = ""

	idCliente = request.POST.get('idClienteObser', False)
	observ = request.POST.get('textAreaObservacion', False)
	observacion = Observacion()
	observacion.fecha = fecha()
	observacion.usuario = request.user
	observacion.texto = observ
	observacion.save()

	cliente = Cliente.objects.get(id=idCliente)

	obcl = ObservacionCliente()
	obcl.observacion = observacion
	obcl.cliente = cliente
	obcl.save()

	context = {'mensaje': mensaje, 'objeto':cliente}
	return render(request, 'sistema/grillaObservaciones.html', context)


@login_required
def getViajesFuturosPorFecha(request):
    mensaje = ""
    date = getAAAAMMDD(request.POST.get('date', False))

    estados_get_seleccionados = request.POST.getlist('estados_selecionados[]', False)
    estados_seleccionados = []
    if estados_get_seleccionados == False:
		estados_seleccionados = [1, 2, 4]
    else:
        for i in estados_get_seleccionados:
			estados_seleccionados.append(i)

	viajes = Viaje.objects.filter(fecha=date).filter(estado__in=estados_seleccionados)
    context = {'mensaje': mensaje, 'viajes':viajes}
    return render(request, 'sistema/grillaViajesFuturos.html', context)

@login_required
def getViajesEnProgresoPorFecha(request):
    mensaje = ""

    date = getAAAAMMDD(request.POST.get('date', False))
    viajes = Viaje.objects.filter(fecha=date)
    context = {'mensaje': mensaje, 'viajes':viajes}
    return render(request, 'sistema/grillaViajesEnProgreso.html', context)

@login_required
def editEstadoViajeAsignaciones(request):
    mensaje = ""
    viajes_get_seleccionado = request.POST.getlist('viajes_seleccionado[]')
    viajes_seleccionados = []
    for i in viajes_get_seleccionado:
        viajes_seleccionados.append(i)
    Viaje.objects.filter(id__in=viajes_seleccionados).update(estado=Estado.objects.get(id=request.POST.get('estado_seleccionado', False)))

    data = {
		'error': '0',
		'msg': mensaje
	}

    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

@login_required
def editEstadoViaje(request):
    mensaje = ""
    viaje = Viaje.objects.get(id=request.POST.get('viaje_seleccionado', False))
    viaje.estado = Estado.objects.get(id=request.POST.get('estado_seleccionado', False))
    viaje.save()
    data = {
		'error': '0',
		'msg': mensaje
	}

    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

@login_required
def guardarMailCliente(request):
	mensaje = ""

	idCliente = request.POST.get('idClienteMail', False)
	nombre = request.POST.get('nombreMailCliente', False)
	mail_txt = request.POST.get('mailCliente', False)
	comentario = request.POST.get('comentarioMailCliente', False)
	mail = Mail()
	mail.mail = mail_txt
	mail.nombre = nombre
	mail.comentario = comentario
	mail.save()

	cliente = Cliente.objects.get(id=idCliente)

	mlcl = MailCliente()
	mlcl.mail = mail
	mlcl.cliente = cliente
	mlcl.save()

	context = {'mensaje': mensaje, 'objeto':cliente}
	return render(request, 'sistema/grillaMails.html', context)

@login_required
def provedor(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/provedor.html', context)

@login_required
def guardarObservacionPersona(request):
	mensaje = ""

	idPersona = request.POST.get('idPersonaObser', False)
	observ = request.POST.get('textAreaObservacion', False)
	observacion = Observacion()
	observacion.fecha = fecha()
	observacion.usuario = request.user
	observacion.texto = observ
	observacion.save()

	persona = Persona.objects.get(id=idPersona)

	obpe = ObservacionPersona()
	obpe.observacion = observacion
	obpe.persona = persona
	obpe.save()

	context = {'mensaje': mensaje, 'objeto':persona}
	return render(request, 'sistema/grillaObservaciones.html', context)

@login_required
def listadoProvedor(request):
	provedores = Persona.objects.filter(tipo_persona__id__in=[3,4])
	context = {'provedores': provedores}
	return render(request, 'sistema/listadoProvedor.html', context)

@login_required
def unidad(request):
	mensaje = ""
	idUnidad = request.GET.get('idUnidad', "")
	unidad = Unidad.objects.get(id=idUnidad)
	owners = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=4),baja=False)
	choferes = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=3),baja=False)
	tipo_licencias = TipoLicencia.objects.all()
	context = {'mensaje': mensaje, 'unidad': unidad, 'owners': owners, 'choferes': choferes, 'tipo_licencias':tipo_licencias}
	return render(request, 'sistema/unidad.html', context)

@login_required
def altaUnidad(request):
	mensaje = ""
	unidad = Unidad()
	unidad.id = 0	
	owners = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=4),baja=False)
	choferes = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=3),baja=False)
	context = {'mensaje': mensaje, 'owners':owners, 'choferes':choferes, 'unidad': unidad}
	return render(request, 'sistema/unidad.html', context)

@login_required
def listadoUnidad(request):
	unidades = Unidad.objects.filter(baja=False)
	context = {'unidades':unidades}
	return render(request, 'sistema/listadoUnidad.html', context)

@login_required
def guardarUnidad(request):
	idUnidad = request.POST.get('idUnidad', "")
	if idUnidad == "0":
		unidad = Unidad()
		vehiculo = Vehiculo()
	else:
		unidad = Unidad.objects.get(id=idUnidad)
		if unidad.vehiculo:
			vehiculo = unidad.vehiculo
		else:
			vehiculo = Vehiculo()

	unidad.identificacion = request.POST.get('identificacion', "")
	unidad.owner = Persona.objects.get(id=request.POST.get('selectOwners', ""))
	unidad.porcentaje_owner = request.POST.get('porcFacturacionOwner', "")
	if request.POST.get('selectChoferes', "") != "":
		unidad.chofer = Persona.objects.get(id=request.POST.get('selectChoferes', ""))
	unidad.porcentaje_chofer = request.POST.get('porcFacturacionChofer', "")
	if request.POST.get('patente', "") != "":
		vehiculo.patente = request.POST.get('patente', "")
		vehiculo.modelo = request.POST.get('modelo', "")
		vehiculo.marca = request.POST.get('marca', "")
		vehiculo.color = request.POST.get('color', "")
		vehiculo.ano = request.POST.get('year', "")
		vehiculo.puertas = request.POST.get('puertas', "")
		vehiculo.nro_motor = request.POST.get('nro_motor', "")
		vehiculo.nro_chasis = request.POST.get('nro_chasis', "")
		vehiculo.save()
		unidad.vehiculo = vehiculo
	unidad.save()
	url = '/sistema/unidad/?idUnidad='+str(unidad.id)
	return redirect(url)

@login_required
def eliminarUnidad(request):
	idUnidad = request.POST.get('idUnidadEliminar', False)
	unidad = Unidad.objects.get(id=idUnidad)
	unidad.baja = True
	unidad.save()
	return redirect('listadoUnidad')

@login_required
def guardarObservacionUnidad(request):
	mensaje = ""

	idUnidad = request.POST.get('idUnidadObser', False)
	observ = request.POST.get('textAreaObservacion', False)
	observacion = Observacion()
	observacion.fecha = fecha()
	observacion.usuario = request.user
	observacion.texto = observ
	observacion.save()

	unidad = Unidad.objects.get(id=idUnidad)

	obcl = ObservacionUnidad()
	obcl.observacion = observacion
	obcl.unidad = unidad
	obcl.save()

	context = {'mensaje': mensaje, 'objeto':unidad}
	return render(request, 'sistema/grillaObservaciones.html', context)

@login_required
def guardarLicenciaUnidad(request):
	idLicencia = request.POST.get('idLicencia', False)
	personaLicencia = request.POST.get('personaLicencia', False)
	descripcion = request.POST.get('descripcionLicencia', False)
	tipo = TipoLicencia.objects.get(id=request.POST.get('tipoLicencia', False))
	fv = request.POST.get('vencimientoLicencia', False)
	fecha = fv[6:10] + fv[3:5] + fv[0:2]

	if idLicencia == "0":
		licencia = Licencia()
	else:
		LicenciaPersona.objects.filter(licencia_id=idLicencia).delete()
		LicenciaVehiculo.objects.filter(licencia_id=idLicencia).delete()
		licencia = Licencia.objects.get(id=idLicencia)

	licencia.comentario = descripcion
	licencia.tipo_licencia = tipo
	licencia.fecha_vencimiento = fecha
	licencia.save()

	if personaLicencia == "chofer":
		lp = LicenciaPersona()
		lp.persona = Persona.objects.get(id=request.POST.get('idChofer', False))
		lp.licencia = licencia
		lp.save()
	elif personaLicencia == "owner":
		lp = LicenciaPersona()
		lp.persona = Persona.objects.get(id=request.POST.get('idOwner', False))
		lp.licencia = licencia
		lp.save()
	else:
		lv = LicenciaVehiculo()
		lv.vehiculo = Vehiculo.objects.get(id=request.POST.get('idVehiculo', False))
		lv.licencia = licencia
		lv.save()

	unidad = Unidad.objects.get(id=request.POST.get('idUnidad', False))
	context = {'unidad':unidad}
	return render(request, 'sistema/grillaLicencias.html', context)

@login_required
def eliminarLicencia(request):
	idLicencia = request.GET.get('idLicencia', False)
	LicenciaPersona.objects.filter(licencia_id=idLicencia).delete()
	LicenciaVehiculo.objects.filter(licencia_id=idLicencia).delete()
	Licencia.objects.get(id=idLicencia).delete()
	return redirect('listadoLicencia')

@login_required
def eliminarLicenciaPropect(request):
	idLicencia = request.POST.get('idLicencia', False)
	idUnidad = request.POST.get('idUnidad', False)
	LicenciaPersona.objects.filter(licencia_id=idLicencia).delete()
	LicenciaVehiculo.objects.filter(licencia_id=idLicencia).delete()
	Licencia.objects.get(id=idLicencia).delete()
	unidad = Unidad.objects.get(id=idUnidad)
	context = {'unidad':unidad}
	return render(request, 'sistema/grillaLicencias.html', context)

@login_required
def contacto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/contacto.html', context)

@login_required
def editaContacto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/contacto.html', context)

@login_required
def listadoContacto(request):
	contactos = Persona.objects.filter(tipo_persona_id=1, baja=False)
	context = {'contactos': contactos}
	return render(request, 'sistema/listadoContacto.html', context)

@login_required
def altaCentroDeCosto(request):
	clientes = Cliente.objects.filter(baja=False)
	tarifarios = Tarifario.objects.filter(baja=False)
	cc = CentroCosto()
	cc.id = 0
	context = {'clientes': clientes, 'tarifarios':tarifarios, 'cc':cc}
	return render(request, 'sistema/centroDeCosto.html', context)

@login_required
def guardarCC(request):
	idCC = request.POST.get('idCC', False)
	cliente_id = request.POST.get('clientes', False)
	tarifario_id = request.POST.get('tarifarios', False)
	codigo = request.POST.get('codigo', False)
	descripcion = request.POST.get('descripcion', False)
	desdeCC = request.POST.get('desdeCC', False)
	hastaCC = request.POST.get('hastaCC', False)

	if idCC == "0":
		cc = CentroCosto()
		request.session['estadoCC'] = 'nuevo'
	else:
		cc = CentroCosto.objects.get(id=idCC)
		request.session['estadoCC'] = 'editado'

	cc.nombre = codigo
	cc.descripcion = descripcion
	cc.cliente = Cliente.objects.get(id=cliente_id)
	cc.tarifario = Tarifario.objects.get(id=tarifario_id)
	cc.fecha_inicio = getAAAAMMDD(desdeCC)
	cc.fecha_fin = getAAAAMMDD(hastaCC)
	cc.save()

	url = '/sistema/centroCosto/?idCC='+str(cc.id)
	return redirect(url)

@login_required
def centroCosto(request):
	estado = request.session.get('estadoCC', '')
	idCC = request.GET.get('idCC', "")
	cc = CentroCosto.objects.get(id=idCC)
	clientes = Cliente.objects.all()
	tarifarios = Tarifario.objects.all()
	request.session['estadoCC'] = ''

	context = {'clientes':clientes, 'estado':estado, 'cc':cc, 'clientes':clientes, 'tarifarios':tarifarios}
	return render(request, 'sistema/centroDeCosto.html', context)

@login_required
def validarCodigoCentroCosto(request):
	codigoCC = request.GET.get('codigoCC', False)
	cc = CentroCosto.objects.filter(nombre=codigoCC)
	if cc:
		data = {'mensaje': 'El codigo seleccionado ya existe.'}
	else:
		data = {'mensaje': ''}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def editaCentroDeCosto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/centroDeCosto.html', context)

@login_required
def listadoCentroDeCosto(request):
	centroCostos = CentroCosto.objects.filter(baja=False)

	context = {'centroCostos': centroCostos}
	return render(request, 'sistema/listadoCentroDeCosto.html', context)

@login_required
def listadoTarifario(request):
	mensaje = ""
	tarifarios = Tarifario.objects.filter(baja=False)
	context = {'tarifarios': tarifarios}
	return render(request, 'sistema/listadoTarifario.html', context)

@login_required
def tarifario(request):
	mensaje = ""
	idTarifario = request.GET.get('idTarifario', "")
	tarifario = Tarifario.objects.get(id=idTarifario)
	context = {'tarifario': tarifario}
	return render(request, 'sistema/tarifario.html', context)

@login_required
def guardarTarifario(request):
	mensaje = ""
	idTarifario = request.POST.get('idTarifario', "")
	nombre = request.POST.get('nombre', "")
	print nombre
	tarifario = Tarifario.objects.get(id=idTarifario)
	tarifario.nombre = nombre
	tarifario.save()
	url = '/sistema/tarifario/?idTarifario='+str(tarifario.id)
	return redirect(url)

@login_required
def editarTarifaTrayecto(request):
	idTarifaTrayecto = request.POST.get('idTarifaTrayecto', "")
	tramoTarifa = TarifaTrayecto.objects.get(id=idTarifaTrayecto)
	context = {'tramoTarifa': tramoTarifa}
	return render(request, 'sistema/tarifaTrayecto.html', context)

@login_required
def editarTarifaExtra(request):
	idTarifaExtra = request.POST.get('idTarifaExtra', "")
	tarifaExtra = TarifaExtra.objects.get(id=idTarifaExtra)
	context = {'tarifaExtra': tarifaExtra}
	return render(request, 'sistema/tarifaExtra.html', context)

@login_required
def guardarTarifaTrayecto(request):
	idTarifario		 = request.POST.get('idTarifario', "")
	idTarifaTrayecto = request.POST.get('idTarifaTrayecto', "")
	
	tarifaTrayecto = TarifaTrayecto.objects.get(id=idTarifaTrayecto)

	for x in range(19):
		cat = x+1
		nameTramo='tramo'+str(cat)
		valor = request.POST.get(nameTramo, "0")
		if valor == "":
			valor = 0
		ttp = tarifaTrayecto.getTTPByCategoria(cat)
		ttp.precio_cliente = valor
		ttp.save()

	tarifario = Tarifario.objects.get(id=idTarifario)
	context = {'tarifario': tarifario}
	return render(request, 'sistema/grillaTrayectoTarifa.html', context)

@login_required
def guardarTarifaExtra(request):
	idTarifario		 = request.POST.get('idTarifario', "")
	idTarifaExtra    = request.POST.get('idTarifaExtra', "")
	
	tarifaExtra = TarifaExtra.objects.get(id=idTarifaExtra)

	for x in range(19):
		cat = x+1
		nameTramo='extra'+str(cat)
		valor = request.POST.get(nameTramo, "0")
		if valor == "":
			valor = 0
		ttp = tarifaExtra.getTTPByCategoria(cat)
		ttp.extra_precio = valor
		ttp.save()

	tarifario = Tarifario.objects.get(id=idTarifario)
	context = {'tarifario': tarifario}
	return render(request, 'sistema/grillaTarifaExtra.html', context)

@login_required
def guardarMasivo(request):
	idTarifario = request.POST.get('idTarifario', "")
	tipoMasivo  = request.POST.get('tipoMasivo', "")
	porcentaje  = request.POST.get('porcentaje', "")

	print idTarifario
	print tipoMasivo
	print porcentaje

	tarifario = Tarifario.objects.get(id=idTarifario)

	if tipoMasivo == "1":
		for tv in tarifario.getTarifaViaje():
			for x in range(19):
				cat = x+1
				ttp = tv.getTTPByCategoria(cat)
				if ttp.precio_cliente:
					valor = ttp.precio_cliente
				else:
					valor = "0"
				ttp.precio_cliente = int(valor) * int(float(porcentaje)) / 100 + int(valor)
				ttp.save()

		nombre_html = "sistema/grillaTrayectoTarifa.html"


	if tipoMasivo == "2":
		for te in tarifario.getTarifaExtra():
			for x in range(19):
				cat = x+1
				ttp = te.getTTPByCategoria(cat)
				if ttp.extra_precio:
					valor = ttp.extra_precio
				else:
					valor = "0"
				ttp.extra_precio = int(valor) * int(float(porcentaje)) / 100 + int(valor)
				ttp.save()

		nombre_html = "sistema/grillaTarifaExtra.html"

	context = {'tarifario': tarifario}
	return render(request, nombre_html, context)


@login_required
def listadoLicencia(request):
	licencias = Licencia.objects.all()
	
	context = {'licencias': licencias}
	return render(request, 'sistema/listadoLicencia.html', context)

@login_required
def altaLicencia(request):
	listaAsignoLicencia = Persona.objects.filter(tipo_persona=3,baja=False)
	tipo_licencias = TipoLicencia.objects.all()
	licencia = Licencia()
	licencia.id = 0
	context = {'licencia': licencia, 'listaAsignoLicencia': listaAsignoLicencia, 'tipo_licencias':tipo_licencias}
	return render(request, 'sistema/licencia.html', context)

@login_required
def licencia(request):
	estado = request.session.get('estadoLicencia', '')
	idLicencia = request.GET.get('idLicencia', "")
	licencia = Licencia.objects.get(id=idLicencia)
	tipo_licencias = TipoLicencia.objects.all()
	asignoLicencia = []
	asignoLicencia.append(licencia.getAsignado())
	tipoAsignadoId = licencia.getAsignadoTipoId()
	tipoAsignado = licencia.getAsignadoTipo()
	request.session['estadoLicencia'] = ''
	context = {'tipo_licencias':tipo_licencias, 'estado':estado, 'licencia':licencia, 'listaAsignoLicencia':asignoLicencia, 'tipoAsignadoId':tipoAsignadoId, 'tipoAsignado':tipoAsignado}
	return render(request, 'sistema/licencia.html', context)

@login_required
def guardarLicencia(request):
	idLicencia = request.POST.get('idLicencia', False)
	tipoPersonaLicencia = request.POST.get('tipoPersonaLicencia', False)
	personaLicencia = request.POST.get('personaLicencia', False)
	tipoLicencia = request.POST.get('tipoLicencia', False)
	vencimientoLicencia = request.POST.get('vencimientoLicencia', False)
	descripcionLicencia = request.POST.get('descripcionLicencia', False)

	if idLicencia == "0":
		licencia = Licencia()
		request.session['estadoLicencia'] = 'nuevo'
	else:
		licencia = Licencia.objects.get(id=idLicencia)
		request.session['estadoLicencia'] = 'editado'

	licencia.comentario = descripcionLicencia
	licencia.tipo_licencia = TipoLicencia.objects.get(id=tipoLicencia)
	licencia.fecha_vencimiento = getAAAAMMDD(vencimientoLicencia)
	licencia.save()

	if idLicencia == "0":
		if tipoPersonaLicencia == "0":
			lp = LicenciaPersona()
			lp.persona = Persona.objects.get(id=personaLicencia)
		elif tipoPersonaLicencia == "1":
			lp = LicenciaPersona()
			lp.persona = Persona.objects.get(id=personaLicencia)
		elif tipoPersonaLicencia == "2":
			lp = LicenciaVehiculo()
			lp.vehiculo = Vehiculo.objects.get(id=personaLicencia)

		lp.licencia = licencia
		lp.save()

	url = '/sistema/licencia/?idLicencia='+str(licencia.id)
	return redirect(url)

@login_required
def getSelectAsignoLicencia(request):
	listaAsignoLicencia = []
	tpl = request.POST.get('tipoPersonaLicencia', False)
	titulo = ""
	if tpl == "0":
		listaAsignoLicencia = Persona.objects.filter(tipo_persona=3,baja=False)
		titulo = "Chofer"
	elif tpl == "1":
		listaAsignoLicencia = Persona.objects.filter(tipo_persona=4,baja=False)
		titulo = "Dueño"
	elif tpl == "2":
		listaAsignoLicencia = Vehiculo.objects.all()
		titulo = "Vehículo"
	context = {'listaAsignoLicencia': listaAsignoLicencia, 'titulo':titulo}
	return render(request, 'sistema/selectAsignoLicencia.html', context)

@login_required
def cargarLocalidad(request):
	cp = request.POST.get('codigoPostal', False)
	localidades = Localidad.objects.filter(codigo_postal=cp)
	context = {'localidades': localidades}
	return render(request, 'sistema/selectLocalidad.html', context)

@login_required
def cargarLocalidadByDestino(request):
	destino_id = request.POST.get('destino_id', False)
	localidad_select_id = request.POST.get('localidad_select_id', '')
	localidades = Localidad.objects.filter(trayectodestino_id=destino_id)
	context = {'localidades': localidades, 'localidad_select_id':localidad_select_id}
	return render(request, 'sistema/selectLocalidadViaje.html', context)

@login_required
def cargarProvincia(request):
	idLocalidad = request.POST.get('idLocalidad', False)
	print idLocalidad
	localidad = Localidad.objects.get(id=idLocalidad)
	print localidad.provincia.id
	provincias = Provincia.objects.filter(id=localidad.provincia.id)
	print provincias
	context = {'provincias':provincias}
	return render(request, 'sistema/selectProvincia.html', context)

@login_required
def exportar(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/exportar.html', context)

@login_required
def usuario(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/usuario.html', context)

@login_required
def listadoAdelanto(request):
	mensaje = ""
	proveedores = Persona.objects.filter(tipo_persona__in=[3,4])
	context = {'mensaje': mensaje, 'proveedores':proveedores}
	return render(request, 'sistema/listadoAdelanto.html', context)

@login_required
def altaAdelanto(request):
	mensaje = ""
	proveedores = Persona.objects.filter(tipo_persona__in=[3,4])
	tipos_adelanto = TipoAdelanto.objects.all()
	adelanto = Adelanto()
	adelanto.id = 0
	context = {'mensaje': mensaje, 'proveedores':proveedores,'tipos_adelanto':tipos_adelanto,'adelanto':adelanto}
	return render(request, 'sistema/adelanto.html', context)

@login_required
def adelanto(request):
	mensaje = ""

	estado = request.session.get('estadoAdelanto', '')
	idAdelanto = request.GET.get('idAdelanto', "")
	adelanto = Adelanto.objects.get(id=idAdelanto)
	tipos_adelanto = TipoAdelanto.objects.all()
	proveedores = Persona.objects.filter(tipo_persona__in=[3,4])

	tipoAdelantoId = adelanto.tipo_adelanto.id
	provedorId = adelanto.proveedor.id
	request.session['estadoAdelanto'] = ''

	context = {'mensaje': mensaje, 
				'proveedores':proveedores,
				'tipos_adelanto':tipos_adelanto, 
				'estado':estado, 
				'idAdelanto':idAdelanto,  
				'tipoAdelantoId':tipoAdelantoId,
				'adelanto':adelanto,
				'provedorId':provedorId
			}
	return render(request, 'sistema/adelanto.html', context)

@login_required
def guardarAdelanto(request):
	mensaje = ""
	idAdelanto = request.POST.get('idAdelanto', False)
	provedor = request.POST.get('provedor', False)
	monto = request.POST.get('monto', False)
	tipoAdelanto = request.POST.get('tipoAdelanto', False)
	descripcion = request.POST.get('descripcion', False)
	fecha = request.POST.get('fecha', False)
	factura = request.POST.get('factura', False)
	
	if idAdelanto == "0":
		adelanto = Adelanto()
		request.session['estadoAdelanto'] = 'nuevo'
	else:
		adelanto = Adelanto.objects.get(id=idAdelanto)
		request.session['estadoAdelanto'] = 'editado'

	adelanto.proveedor = Persona.objects.get(id=provedor)
	adelanto.monto = monto
	adelanto.tipo_adelanto = TipoAdelanto.objects.get(id=tipoAdelanto)
	adelanto.descripcion = descripcion
	adelanto.fecha = getAAAAMMDD(fecha)
	adelanto.factura = factura
	adelanto.save()

	url = '/sistema/adelanto/?idAdelanto='+str(adelanto.id)
	return redirect(url)

@login_required
def buscarAdelantos(request):

	fechaDesde = request.POST.get('desde', False)
	fechaHasta = request.POST.get('hasta', False)
	provedor = request.POST.get('provedor', False)

	fechaDesde =  getAAAAMMDD(fechaDesde)
	fechaHasta =  getAAAAMMDD(fechaHasta)

	adelantos = []
	if provedor:
		print 'if'
		adelantos = Adelanto.objects.filter(proveedor_id=provedor,fecha__gte=fechaDesde, fecha__lte=fechaHasta)
	else:
		print 'else'
		adelantos = Adelanto.objects.filter(fecha__gte=fechaDesde, fecha__lte=fechaHasta)

	context = {'adelantos': adelantos}
	return render(request, 'sistema/grillaAdelantos.html', context)

@login_required
def eliminarAdelanto(request):
	idAdelanto = request.GET.get('idAdelanto', False)
	Adelanto.objects.get(id=idAdelanto).delete()
	data = {'return': 'success'}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')


@login_required
def facturarAdelantos(request):
	idAdelantos = request.POST.get('idAdelantos', False)
	numeroFactura = request.POST.get('numeroFactura', False)
	idsList = []
	for ids in idAdelantos.split("-"):
		if ids:
			idsList.append(int(ids))

	adelantos = Adelanto.objects.filter(id__in=idsList)
	for a in adelantos:
		a.factura = numeroFactura
		a.save()

	data = {'return': 'success'}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def listadoFactClientes(request):
	clientes = Cliente.objects.filter(baja=False)
	categorias = CategoriaViaje.objects.all()
	condicionesPago = CondicionPago.objects.all()
	context = {'clientes': clientes, 'categorias':categorias, 'condicionesPago':condicionesPago}
	return render(request, 'sistema/listadoFactClientes.html', context)

@login_required
def cargarCentrosDeCosto(request):
	idCliente = request.GET.get('idCliente', False)
	centrosDeCosto = []
	if idCliente:
		centrosDeCosto = CentroCosto.objects.filter(cliente_id=idCliente)

	context = {'centrosDeCosto': centrosDeCosto}
	return render(request, 'sistema/selectCentroCostos.html', context)

@login_required
def cargarSolicitantes(request):
	idCliente = request.GET.get('idCliente', False)
	solicitantes = []
	if idCliente:
		solicitantes = Persona.objects.filter(personacliente__cliente_id=idCliente, tipo_persona_id=1)

	context = {'solicitantes': solicitantes}
	return render(request, 'sistema/selectSolicitantes.html', context)

@login_required
def cargarFactura(request):
	idCliente = request.GET.get('idCliente', False)
	facturas = []
	if idCliente:
		viajes = FacturaViaje.objects.filter(viaje__cliente_id=idCliente).order_by('fact_cliente')
		for v in viajes:
			if v.fact_cliente not in facturas:
				if v.fact_cliente:
					facturas.append(v.fact_cliente)

	context = {'facturas': facturas}
	return render(request, 'sistema/selectFacturas.html', context)

@login_required
def cargarFacturaUnidad(request):
	idUnidad = request.GET.get('idUnidad', False)
	facturas = []
	if idUnidad:
		viajes = FacturaViaje.objects.filter(viaje__unidad_id=idUnidad).order_by('fact_proveedor')
		for v in viajes:
			if v.fact_proveedor not in facturas:
				if v.fact_proveedor:
					facturas.append(v.fact_proveedor)

	context = {'facturas': facturas}
	return render(request, 'sistema/selectFacturas.html', context)

@login_required
def cargarProforma(request):
	idCliente = request.GET.get('idCliente', False)
	proformas = []
	if idCliente:
		viajes = FacturaViaje.objects.filter(viaje__cliente_id=idCliente).order_by('prof_cliente')
		for v in viajes:
			if v.prof_cliente in proformas:
				pass
			else:
				if v.prof_cliente:
					proformas.append(v.prof_cliente)

	context = {'proformas': proformas}
	return render(request, 'sistema/selectProformas.html', context)

@login_required
def cargarProveedores(request):
	idUnidad = request.GET.get('idUnidad', False)
	proveedores = []
	if idUnidad:
		unidad = Unidad.objects.get(id=idUnidad)
		if unidad.chofer:
			proveedores.append(unidad.chofer)
		if unidad.owner:
			proveedores.append(unidad.owner)
	context = {'proveedores': proveedores}
	return render(request, 'sistema/selectProveedores.html', context)

@login_required
def buscarFacturacionCliente(request):
	idCliente 		= request.POST.get('cliente', False)
	categorias 		= request.POST.get('categorias', False)
	centroDeCosto 	= request.POST.get('centroDeCosto', False)
	condEspecial 	= request.POST.get('condEspecial', False)
	solicitantes 	= request.POST.get('solicitantes', False)
	facturas 		= request.POST.get('facturas', False)
	proformas 		= request.POST.get('proformas', False)
	desde 			= request.POST.get('desde', False)
	hasta 			= request.POST.get('hasta', False)

	fechaDesde =  getAAAAMMDD(desde)
	fechaHasta =  getAAAAMMDD(hasta)

	listaviajes = []

	catList = []
	if categorias != "null":
		for c in categorias.split(","):
			catList.append(int(c))

	ccList = []
	if centroDeCosto != "null":
		for c in centroDeCosto.split(","):
			ccList.append(int(c))

	facList = []
	if facturas != "null":
		for c in facturas.split(","):
			facList.append(c)
	
	proList = []
	if proformas != "null":
		for c in proformas.split(","):
			proList.append(c)

	solList = []
	if solicitantes != "null":
		for c in solicitantes.split(","):
			solList.append(int(c))

	viajes = Viaje.objects.filter(cliente_id=idCliente,estado_id=7,fecha__gte=fechaDesde, fecha__lte=fechaHasta)
	if catList:
		viajes = viajes.filter(categoria_viaje_id__in=catList)
	if ccList:
		viajes = viajes.filter(centro_costo_id__in=ccList)
	if solList:
		viajes = viajes.filter(cliente__personacliente__persona_id__in=solList)
	
	if condEspecial == "1":
		q_ids = [o.id for o in viajes if o.getMontoEstacionCliente() == 0]
		viajes = viajes.filter(id__in=q_ids)
	elif condEspecial == "2":
		q_ids = [o.id for o in viajes if o.getMontoEstacionCliente() > 0]
		viajes = viajes.filter(id__in=q_ids)

	if facList:
		q_ids = [o.id for o in viajes if o.getFacturaCliente() in facList]
		viajes = viajes.filter(id__in=q_ids)

	if proList:
		q_ids = [o.id for o in viajes if o.getProforma() in proList]
		viajes = viajes.filter(id__in=q_ids)

	context = {'viajes': viajes}
	return render(request, 'sistema/grillaFacturacionCliente.html', context)

@login_required
def buscarFacturacionProveedor(request):
	idUnidad 		= request.POST.get('unidad', False)
	condEspecial 	= request.POST.get('condEspecial', False)
	facturas 		= request.POST.get('facturas', False)
	proveedor 		= request.POST.get('proveedor', False)
	desde 			= request.POST.get('desde', False)
	hasta 			= request.POST.get('hasta', False)

	fechaDesde =  getAAAAMMDD(desde)
	fechaHasta =  getAAAAMMDD(hasta)

	listaviajes = []

	facList = []
	if facturas != "null":
		for c in facturas.split(","):
			facList.append(c)

	viajes = Viaje.objects.filter(unidad_id=idUnidad,estado_id=7,fecha__gte=fechaDesde, fecha__lte=fechaHasta)

	if facList:
		q_ids = [o.id for o in viajes if o.getFacturaProveedor() in facList]
		viajes = viajes.filter(id__in=q_ids)

	context = {'viajes': viajes}
	return render(request, 'sistema/grillaFacturacionProveedor.html', context)

@login_required
def facturarClientes(request):
	idViajes 			= request.POST.get('idViajes', False)
	numeroFactrura		= request.POST.get('numeroFactura', False)
	primernumeroFactura = request.POST.get('primernumeroFactura', False)
	idsList = []
	for ids in idViajes.split("-"):
		if ids:
			idsList.append(int(ids))

	viajes = Viaje.objects.filter(id__in=idsList)
	for v in viajes:
		if v.facturaviaje_set.all():
			fv = v.facturaviaje_set.all()[0]
		else:
			fv = FacturaViaje()
			fv.viaje = v

		fv.fact_cliente = primernumeroFactura + "-" + numeroFactrura
		fv.save()

	data = {'return': 'success'}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def facturarProveedores(request):
	idViajes 			= request.POST.get('idViajes', False)
	numeroFactrura		= request.POST.get('numeroFactura', False)
	primernumeroFactura = request.POST.get('primernumeroFactura', False)
	idsList = []
	for ids in idViajes.split("-"):
		if ids:
			idsList.append(int(ids))

	viajes = Viaje.objects.filter(id__in=idsList)
	for v in viajes:
		if v.facturaviaje_set.all():
			fv = v.facturaviaje_set.all()[0]
		else:
			fv = FacturaViaje()
			fv.viaje = v

		fv.fact_proveedor = primernumeroFactura + "-" + numeroFactrura
		fv.save()

	data = {'return': 'success'}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def proformarClientes(request):
	idViajes = request.POST.get('idViajes', False)

	facturasViaje = FacturaViaje.objects.all().order_by('-prof_cliente')
	if facturasViaje:
		numeroProforma = facturasViaje[0].prof_cliente
		if numeroProforma:
			numeroProforma = int(numeroProforma) + 1
		else:
			numeroProforma = 1
	else:
		numeroProforma = 1

	idsList = []
	for ids in idViajes.split("-"):
		if ids:
			idsList.append(int(ids))

	viajes = Viaje.objects.filter(id__in=idsList)
	for v in viajes:
		if v.facturaviaje_set.all():
			fv = v.facturaviaje_set.all()[0]
		else:
			fv = FacturaViaje()
			fv.viaje = v

		fv.prof_cliente = numeroProforma
		fv.save()

	data = {'return': numeroProforma}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')

@login_required
def listadoFactProvedores(request):
	unidades = Unidad.objects.all()

	context = {'unidades': unidades}
	return render(request, 'sistema/listadoFactProvedores.html', context)

@login_required
def cargarFacturaProveedor(request):
	idUnidad = request.GET.get('idUnidad', False)
	facturas = []
	if idUnidad:
		viajes = FacturaViaje.objects.filter(viaje__unidad_id=idUnidad).order_by('fact_proveedor')
		for v in viajes:
			if v.fact_proveedor not in facturas:
				if v.fact_proveedor:
					facturas.append(v.fact_proveedor)

	context = {'facturas': facturas}
	return render(request, 'sistema/selectFacturas.html', context)

@login_required
def cargarMenu(request):
	print request.user
	permisos = [x.name for x in Permission.objects.filter(user=request.user)]
	print permisos
	if 'unidades' in permisos:
		menu_file = "sistema/unidadesMenu.html"
	if 'operaciones' in permisos:
		menu_file = "sistema/operacionesMenu.html"
	if 'finanzas' in permisos:
		menu_file = "sistema/finanzasMenu.html"
	if 'superuser' in permisos:
		menu_file = "sistema/superUserMenu.html"

	context = {'facturas': ''}
	return render(request, menu_file, context)

# devuelve AAAAMMDD
def fecha():
	import time
	return time.strftime("%Y%m%d%H%M")

def getAAAAMMDD(fecha):
	return fecha[6:10] + fecha[3:5] + fecha[0:2]

@register.filter
def get_tarifa_by_cat(tarifaTrayecto, idCat):
    return tarifaTrayecto.getTarifaByCategoria(idCat)

@register.filter
def get_tarifa_extra_by_cat(tarifaExtra, idCat):
    return tarifaExtra.getTarifaExtraByCategoria(idCat)