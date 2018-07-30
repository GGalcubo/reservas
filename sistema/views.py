# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calle, TrayectoDestino, TipoObservacion, Localidad, Provincia, Tarifario, Cliente, Telefono, TipoTelefono, TelefonoCliente, Unidad, Estado, Viaje, Trayecto, Persona, CentroCosto, CategoriaViaje, Observacion, ObservacionCliente, TipoPersona, Vehiculo, ObservacionUnidad, ObservacionViaje, Mail, MailCliente, TelefonoPersona, TipoLicencia, Licencia, LicenciaPersona, LicenciaVehiculo
from django.http import HttpResponse

import json

@login_required
def importar_calles(request):
	Calle.objects.all().delete()
	Partido.objects.all().delete()
	Provincia.objects.all().delete()

	import csv
	with open('calles.csv') as csvfile:
		reader = csv.reader(csvfile)
		cont = 0
		for row in reader:
			cont = cont + 1
			if cont != 1:
				try:
					alt_desde = row[0]
					alt_hasta = row[1]
					calle_csv = row[3]
					part_csv = row[6]
					prov_csv = row[7]
				
				
					try:
						provincia = Provincia.objects.get(nombre=prov_csv)
					except Provincia.DoesNotExist:
						provincia = Provincia(nombre=prov_csv)
						provincia.save()
		
					try:
						partido = Partido.objects.get(nombre=part_csv)
					except Partido.DoesNotExist:
						partido = Partido(nombre=part_csv, provincia=provincia)
						partido.save()

					calle = Calle()
					calle.nombre = calle_csv
					calle.altura_desde = alt_desde
					calle.altura_hasta = alt_hasta
					calle.partido = partido
					calle.save()

				except Exception as e:
					print str(cont) + str(e)		

			





	mensaje = ""

	context = { 'mensaje':mensaje }
	return render(request, 'sistema/operaciones.html', context)

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

    context = {'mensaje': mensaje,'clientes':clientes, 'tipoobservacion':tipoobservacion, 'unidades':unidades, 'estados':estados, 'categoria_viajes':categoria_viajes,'destinos':destinos,'localidades':localidades,'provincias':provincias, 'es_nuevo':es_nuevo, 'viaje':viaje}
    return render(request, 'sistema/viaje.html', context)

@login_required
def editaViaje(request):
    mensaje = ""

    es_nuevo = 0

    id_viaje = request.GET.get('idViaje', "")
    viaje = Viaje.objects.get(id=id_viaje)

    clientes = Cliente.objects.all()
    unidades = Unidad.objects.all()
    estados = Estado.objects.all()
    categoria_viajes = CategoriaViaje.objects.all()
    destinos = TrayectoDestino.objects.all()
    localidades = Localidad.objects.all()
    provincias = Provincia.objects.all()
    observaciones = Observacion.objects.all()
    tipoobservacion = TipoObservacion.objects.all()
    trayectos = Trayecto.objects.filter(viaje_id=id_viaje)

    context = {'mensaje': mensaje,'clientes':clientes, 'tipoobservacion':tipoobservacion, 'unidades':unidades, 'estados':estados, 'categoria_viajes':categoria_viajes,'destinos':destinos,'localidades':localidades,'provincias':provincias, 'es_nuevo':es_nuevo, 'viaje':viaje, 'trayectos':trayectos}
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
    viaje.solicitante 			= solicitante.nombre + '' + solicitante.apellido
    viaje.centro_costo 			= CentroCosto.objects.get(id=request.POST.get('centro_costos', False))
    pasajero 					= Persona.objects.get(id=request.POST.get('pasajero', False))
    viaje.pasajero 				= pasajero.nombre + '' + pasajero.apellido
    fecha 						= request.POST.get('fecha', "")
    viaje.fecha 				= fecha[6:10] + fecha[3:5] + fecha[0:2]
    viaje.hora 					= request.POST.get('hora', "")
    viaje.hora_estimada 		= request.POST.get('hora_estimada', "")
    viaje.costo_prov 			= request.POST.get('costo_proveedor', "")
    viaje.tarifapasada 			= request.POST.get('tarifa_pasada', "")
    #viaje.comentario_chofer = request.POST.get('comentario_chofer', "")
    unidad 						= id=request.POST.get('unidad', '')
    if unidad != '':
        viaje.unidad 			= Unidad.objects.get(id=request.POST.get('unidad', ''))
    viaje.espera 				= request.POST.get('espera', "")
    viaje.peaje_total 			= request.POST.get('peaje', "")
    viaje.Otros_tot 			= request.POST.get('otros', "")
    viaje.estacionamiento_total = request.POST.get('estacionamiento', "")
    viaje.save()

    data = {
        'error': '0',
        'msg': mensaje
    }

    if es_nuevo == "1":
        data['id_viaje'] = Viaje.objects.latest('id').id

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
	context = {'mensaje': mensaje, 'cliente':cliente, 'tarifarios':tarifarios}
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
    viajes = Viaje.objects.filter(fecha=date)

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
	mensaje = ""

	context = {'mensaje': mensaje}
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
	localidades = Localidad.objects.filter(provincia_id=destino_id)
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

# devuelve AAAAMMDD
def fecha():
	import time
	return time.strftime("%Y%m%d%H%M")

def getAAAAMMDD(fecha):
	return fecha[6:10] + fecha[3:5] + fecha[0:2]