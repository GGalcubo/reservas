# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

    context = {'mensaje': mensaje, 'viajes': viajes, 'clientes': clientes, 'unidades': unidades, 'estados': estados,'categoria_viajes': categoria_viajes}
    return render(request, 'sistema/operaciones.html', context)

@login_required
def asignaciones(request):
	mensaje = ""

	context = { 'mensaje':mensaje }
	return render(request, 'sistema/asignaciones.html', context)

@login_required
def altaViaje(request):
    mensaje = ""

    es_nuevo = 1

    viaje = Viaje()
    viaje.id = 0

    clientes = Cliente.objects.all()
    unidades = Unidad.objects.all()
    estados = Estado.objects.all()
    categoria_viajes = CategoriaViaje.objects.all()
    localidades = Localidad.objects.all()
    provincias = Provincia.objects.all()
    destinos = TrayectoDestino.objects.all()
    observaciones = Observacion.objects.all()
    tipoobservacion = TipoObservacion.objects.all()
    tipo_pago = TipoPagoViaje.objects.all()

    context = {'mensaje': mensaje,'clientes':clientes, 'tipoobservacion':tipoobservacion, 'tipo_pago':tipo_pago, 'unidades':unidades, 'estados':estados, 'categoria_viajes':categoria_viajes,'destinos':destinos,'localidades':localidades,'provincias':provincias, 'es_nuevo':es_nuevo, 'viaje':viaje}
    return render(request, 'sistema/viaje.html', context)

@login_required
def editaViaje(request):
    mensaje = ""

    es_nuevo = 0

    id_viaje = request.GET.get('idViaje', "")
    viaje = Viaje.objects.get(id=id_viaje)
    # used to generate random unique id
    import uuid
    uid = uuid.uuid4()

    clientes = Cliente.objects.all()
    unidades = Unidad.objects.all()
    estados = Estado.objects.all()
    categoria_viajes = CategoriaViaje.objects.all()
    destinos = TrayectoDestino.objects.all()
    localidades = Localidad.objects.all()
    provincias = Provincia.objects.all()
    observaciones = Observacion.objects.all()
    tipoobservacion = TipoObservacion.objects.all()
    tipo_pago = TipoPagoViaje.objects.all()
    trayectos = Trayecto.objects.filter(viaje_id=id_viaje)
    itemsviaje = ItemViaje.objects.filter(viaje_id=id_viaje)

    context = {'mensaje': mensaje,'clientes':clientes, 'uid':uid, 'tipoobservacion':tipoobservacion, 'tipo_pago':tipo_pago, 'itemsviaje':itemsviaje, 'unidades':unidades, 'estados':estados, 'categoria_viajes':categoria_viajes,'destinos':destinos,'localidades':localidades,'provincias':provincias, 'es_nuevo':es_nuevo, 'viaje':viaje, 'trayectos':trayectos}
    return render(request, 'sistema/viaje.html', context)


@login_required
def guardarViaje(request):

    es_nuevo = request.POST.get('es_nuevo', "1")

    if es_nuevo == "1":
        viaje = Viaje()
        mensaje = 'Se dio de alta el viaje '
    else:
        viaje = Viaje.objects.get(id=request.POST.get('idViaje', False))
        mensaje = 'Se actualizo el viaje '

    viaje.estado 				= Estado.objects.get(id=request.POST.get('estado', False))
    viaje.cliente 				= Cliente.objects.get(id=request.POST.get('cliente', False))
    viaje.categoria_viaje 		= CategoriaViaje.objects.get(id=request.POST.get('categoria_viaje', False))
    solicitante 				= Persona.objects.get(id=request.POST.get('contacto', False))
    viaje.solicitante 			= solicitante.nombre + ' ' + solicitante.apellido
    viaje.centro_costo 			= CentroCosto.objects.get(id=request.POST.get('centro_costos', False))
    pasajero 					= Persona.objects.get(id=request.POST.get('pasajero', False))
    viaje.pasajero 				= pasajero.nombre + '' + pasajero.apellido
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

    guardaItemViaje(request.POST.get('importe_efectivo', ''),12,1,viaje)
    guardaItemViaje(request.POST.get('otros', ''),16,1,viaje)
    guardaItemViaje(request.POST.get('peaje', ''),15,1,viaje)
    guardaItemViaje(request.POST.get('estacionamiento', ''),11,1,viaje)
    guardaItemViaje(request.POST.get('costo_proveedor', ''),8,1,viaje)
    #guardaItemViaje(request.POST.get('espera', ''),8,request.POST.get('tiempo_espera', ''),viaje)

    guardarObsViaje(request.POST.get('comentario_chofer', ""), viaje, request)

    if es_nuevo == "1":
        data = {'url': '/sistema/editaViaje/?idViaje=' + str(viaje.id)}

    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

def guardaItemViaje(input_text,tipo_item_viaje,cant,viaje):
    monto = input_text
    tipo_item_viaje = TipoItemViaje.objects.get(id=tipo_item_viaje)
    try:
        item_viaje_otros = ItemViaje.objects.get(viaje=viaje,tipo_items_viaje=tipo_item_viaje)
        if monto == '':
            monto = 0
    except ItemViaje.DoesNotExist:
        if monto == '':
            return
        item_viaje_otros = ItemViaje()

    item_viaje_otros.cant = cant
    item_viaje_otros.monto_s_iva = monto
    item_viaje_otros.viaje = viaje

    item_viaje_otros.monto_iva = int(monto) * int(tipo_item_viaje.iva_pct)
    item_viaje_otros.tipo_items_viaje = tipo_item_viaje
    item_viaje_otros.save()

def guardarObsViaje(input_text, viaje, request):

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

    if request.method == 'POST':
        import uuid

        if not request.POST[u"uid"]:
            return HttpResponseBadRequest("UID not specified.")
        uid = request.POST[u"uid"]

        file = request.FILES[u'files[]']

        error = False

        # file size
        if file.size > options["maxfilesize"]:
            error = "maxFileSize"
        if file.size < options["minfilesize"]:
            error = "minFileSize"
            # allowed file type
        if file.content_type not in options["acceptedformats"]:
            error = "acceptFileTypes"

        response_data = {
            "name": file.name,
            "size": file.size,
            "type": file.content_type
        }

        if error:
            response_data["error"] = error
            response_data = json.dumps([response_data])
            return HttpResponse(response_data, mimetype='application/json')

        #filename = os.path.join('adjuntos/', str(uuid.uuid4()) + file.name)

        adjunto = Adjunto()
        adjunto.upload = request.FILES[u'files[]']
        adjunto.fecha = '2018'
        adjunto.save()

        viajeAdjunto = AdjuntoViaje()
        viajeAdjunto.adjunto = adjunto
        viajeAdjunto.viaje_id = request.POST[u"idViaje"]
        viajeAdjunto.save()

        import urllib

        #response_data["delete_url"] = request.path + "?" + urllib.urlencode(
            #{"f": uid + "/" + os.path.split(filename)[1]})
        #response_data["delete_type"] = "POST"
        response_data["url"] = adjunto.upload.url
        response_data["thumbnailUrl"] = adjunto.upload.url

        response_data = {
            'files': [response_data]
        }

        response_data = json.dumps(response_data)
        response_type = "application/json"
        if "text/html" in request.META["HTTP_ACCEPT"]:
            response_type = "text/html"

        # return the data to the uploading plugin
        return HttpResponse(response_data, content_type=response_type)
    else:

        idViaje = request.GET.get('idViaje', '')
        viajeAdjuntos = AdjuntoViaje.objects.filter(viaje_id=idViaje)

        adjunto = ''
        nombre = ''
        adjuntos = {}
        data = {
            'files': []
        }
        for item in viajeAdjuntos:
            data['files'].append({
                'url':item.adjunto.upload.url,
                'name':item.adjunto.upload.name,
                'thumbnailUrl':item.adjunto.upload.url,
                'delete_url': item.adjunto.upload.url,
                'delete_type': "POST"
            })


        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

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

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoTarifario.html', context)

@login_required
def tarifario(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/tarifario.html', context)

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
	print numeroFactura
	idsList = []
	print idAdelantos.split("-")
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
	centrosDeCosto = CentroCosto.objects.filter(cliente_id=idCliente)
	context = {'centrosDeCosto': centrosDeCosto}
	return render(request, 'sistema/selectCentroCostos.html', context)

@login_required
def cargarSolicitanteDeCosto(request):
	idCliente = request.GET.get('idCliente', False)
	centrosDeCosto = CentroCosto.objects.filter(cliente_id=idCliente)
	context = {'centrosDeCosto': centrosDeCosto}
	return render(request, 'sistema/selectSolicitantes.html', context)

@login_required
def cargarFactura(request):
	idCliente = request.GET.get('idCliente', False)
	viajes = FacturaViaje.objects.filter(viaje__cliente_id=idCliente).order_by('fact_cliente')
	facturas = []
	for v in viajes:
		if v.fact_cliente in facturas:
			pass
		else:
			facturas.append(v.fact_cliente)

	context = {'facturas': facturas}
	return render(request, 'sistema/selectFacturas.html', context)

@login_required
def cargarProforma(request):
	idCliente = request.GET.get('idCliente', False)
	viajes = FacturaViaje.objects.filter(viaje__cliente_id=idCliente).order_by('prof_cliente')
	proformas = []
	for v in viajes:
		if v.prof_cliente in proformas:
			pass
		else:
			proformas.append(v.prof_cliente)
	context = {'proformas': proformas}
	return render(request, 'sistema/selectProformas.html', context)

@login_required
def buscarFacturacionCliente(request):
	idCliente 		= request.POST.get('cliente', False)
	categorias 		= request.POST.get('categorias', False)
	centroDeCosto 	= request.POST.get('centroDeCosto', False)
	condEspecial 	= request.POST.get('condEspecial', False)
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
			ccLista.append(int(c))

	ceList = []
	if condEspecial != "null":
		for c in condEspecial.split(","):
			ceList.append(int(c))

	facList = []
	if facturas != "null":
		for c in facturas.split(","):
			facList.append(int(c))
	
	proList = []
	if proformas != "null":
		for c in proformas.split(","):
			proList.append(int(c))

	viajes = Viaje.objects.filter(cliente_id=idCliente,fecha__gte=fechaDesde, fecha__lte=fechaHasta)
	if catList:
		viajes = viajes.filter(categoria_viaje_id__in=catList)
	if ccList:
		viajes = viajes.filter(centro_costo_id__in=ccList)
	
	context = {'viajes': viajes}
	return render(request, 'sistema/grillaFacturacionCliente.html', context)

@login_required
def listadoFactProvedores(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoFactProvedores.html', context)

# devuelve AAAAMMDD
def fecha():
	import time
	return time.strftime("%Y%m%d%H%M")

def getAAAAMMDD(fecha):
	return fecha[6:10] + fecha[3:5] + fecha[0:2]