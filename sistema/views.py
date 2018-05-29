# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calle, Localidad, Provincia, CategoriaCliente, Tarifario, Cliente, Telefono, TipoTelefono, TelefonoCliente, Unidad, Estado, Viaje, Persona, CentroCosto, CategoriaViaje, Observacion, ObservacionCliente, TipoPersona, Vehiculo
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
	return render(request, 'sistema/dashboard.html', context)

@login_required
def dashboard(request):
	mensaje = ""

	context = { 'mensaje':mensaje }
	return render(request, 'sistema/dashboard.html', context)

@login_required
def operaciones(request):
	mensaje = ""

	context = { 'mensaje':mensaje }
	return render(request, 'sistema/operaciones.html', context)

@login_required
def viaje(request):
	mensaje = ""

	es_nuevo = 1

	clientes = Cliente.objects.all()
	unidades = Unidad.objects.all()
	estados = Estado.objects.all()
	categoria_viajes = CategoriaViaje.objects.all()

	context = {'mensaje': mensaje, 'clientes':clientes, 'unidades':unidades, 'estados':estados, 'categoria_viajes':categoria_viajes, 'es_nuevo':es_nuevo}
	return render(request, 'sistema/viaje.html', context)


@login_required
def guardarViaje(request):

	viaje = Viaje()
	viaje.estado = Estado.objects.get(id=request.POST.get('estado', False))
	viaje.cliente = Cliente.objects.get(id=request.POST.get('cliente', False))
	viaje.categoria_viaje = CategoriaViaje.objects.get(id=request.POST.get('categoria_viaje', False))
	viaje.solicitante = Persona.objects.get(id=request.POST.get('solicitante', False))
	viaje.centro_costo = CentroCosto.objects.get(id=request.POST.get('centro_costos', False))
	viaje.pasajero = Persona.objects.get(id=request.POST.get('pasajero', False))
	viaje.fecha = request.POST.get('fecha', "")
	viaje.hora = request.POST.get('hora', "")
	#viaje.costo_provedor = request.POST.get('costo_provedor', "")
	#viaje.tarifa_pasada = request.POST.get('tarifa_pasada', "")
	#viaje.comentario_chofer = request.POST.get('comentario_chofer', "")
	viaje.unidad = Unidad.objects.get(id=request.POST.get('unidad', False))
	#viaje.espera = request.POST.get('espera', "")
	viaje.peaje_total = request.POST.get('peaje', "")
	viaje.Otros_tot = request.POST.get('otros', "")
	viaje.estacionamiento_total = request.POST.get('estacionamiento', "")
	viaje.save()

	data = {
		'error': '0',
		'msg': 'Los datos han sido guardados correctamente.'
	}
	dump = json.dumps(data)
	return HttpResponse(dump, content_type='application/json')


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
def listadoCliente(request, **kwargs):
	mensajeSuccess = request.session.get('mensajeSuccess', '')
	try:
		del request.session['mensajeSuccess']
	except KeyError:
		pass
	clientes = Cliente.objects.filter(baja=False)
	context = {'clientes': clientes, 'mensajeSuccess':mensajeSuccess}
	return render(request, 'sistema/listadoCliente.html', context)

@login_required
def cliente(request):
	mensaje = ""
	idCliente = request.GET.get('idCliente', "")
	cliente = Cliente.objects.get(id=idCliente)
	tarifarios = Tarifario.objects.all()
	categorias = CategoriaCliente.objects.all()

	context = {'mensaje': mensaje, 'cliente':cliente, 'tarifarios':tarifarios, 'categorias':categorias}
	return render(request, 'sistema/cliente.html', context)

@login_required
def altaCliente(request):
	mensaje = ""
	cliente = Cliente()
	cliente.id = 0
	tarifarios = Tarifario.objects.all()
	categorias = CategoriaCliente.objects.all()
	context = {'mensaje': mensaje, 'tarifarios':tarifarios, 'categorias':categorias, 'cliente': cliente}
	return render(request, 'sistema/cliente.html', context)


@login_required
def guardarCliente(request):
	idCliente = request.POST.get('idCliente', "")
	if idCliente == "0":
		cliente = Cliente()
		tel = Telefono()
		mensaje = 'Se dio de alta el cliente '
	else:
		cliente = Cliente.objects.get(id=idCliente)
		tel = cliente.telefonocliente_set.all()[0].telefono
		mensaje = 'Se actualizo el cliente '

	cliente.razon_social = request.POST.get('razonSocial', "")
	cliente.cuil = request.POST.get('cuil', "")
	cliente.calle = request.POST.get('calle', "")
	cliente.altura = request.POST.get('altura',"")
	cliente.piso = request.POST.get('piso', "")
	cliente.depto = request.POST.get('depto', "")
	cliente.cp = request.POST.get('cp', "")
	cliente.categoria = CategoriaCliente.objects.get(id=request.POST.get('categorias', False))
	cliente.tarifario = Tarifario.objects.get(id=request.POST.get('tarifarios', False))
	cliente.save()

	
	tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")
	tel.numero = request.POST.get('telefono', False)
	tel.save()

	if idCliente == "0":
		telcli = TelefonoCliente()
		telcli.cliente = cliente
		telcli.telefono = tel
		telcli.save()

	request.session['mensajeSuccess'] = mensaje + cliente.razon_social

	return redirect('listadoCliente')

@login_required
def editaCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/cliente.html', context)

@login_required
def eliminarCliente(request):
	idCliente = request.POST.get('idClienteEliminar', False)
	print '--------------'
	print idCliente
	cliente = Cliente.objects.get(id=idCliente)
	cliente.baja = True
	cliente.save()
	request.session['mensajeSuccess'] = 'Se elimino el cliente ' + cliente.razon_social

	return redirect('listadoCliente')


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

	context = {'mensaje': mensaje, 'cliente':cliente}
	return render(request, 'sistema/grillaObservaciones.html', context)

@login_required
def provedor(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/provedor.html', context)

@login_required
def listadoProvedor(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoProvedor.html', context)

@login_required
def unidad(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/unidad.html', context)

@login_required
def altaUnidad(request):
	mensaje = ""
	unidad = Unidad()
	unidad.id = 0	
	owners = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=1))
	choferes = Persona.objects.filter(tipo_persona_id=TipoPersona.objects.get(id=2))
	context = {'mensaje': mensaje, 'owners':owners, 'choferes':choferes, 'unidad': unidad}
	return render(request, 'sistema/unidad.html', context)

@login_required
def listadoUnidad(request):
	mensaje = ""
	unidades = Unidad.objects.filter(baja=False)
	context = {'mensaje': mensaje, 'unidades':unidades}
	return render(request, 'sistema/listadoUnidad.html', context)

@login_required
def guardarUnidad(request):
	idUnidad = request.POST.get('idUnidad', "")
	if idUnidad == "0":
		unidad = Unidad()
		vehiculo = Vehiculo()
		mensaje = 'Se dio de alta launidad '
	else:
		unidad = Unidad.objects.get(id=idUnidad)
		vehiculo = unidad.vehiculo
		mensaje = 'Se actualizo la unidad '

	unidad.identificacion = request.POST.get('identificador', "")
	unidad.owner = Persona.objects.get(id=request.POST.get('selectOwners', ""))
	unidad.porcentaje_owner = request.POST.get('porcFacturacionOwner', "")
	unidad.chofer = Persona.objects.get(id=request.POST.get('selectChoferes', ""))
	unidad.porcentaje_chofer = request.POST.get('porcFacturacionChofer', "")
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

	request.session['mensajeSuccess'] = mensaje + unidad.identificador

	return redirect('listadoUnidad')

@login_required
def eliminarUnidad(request):
	idUnidad = request.POST.get('idUnidadEliminar', False)
	unidad = Unidad.objects.get(id=idUnidad)
	unidad.baja = True
	unidad.save()
	request.session['mensajeSuccess'] = 'Se elimino la unidad ' + unidad.identificacion

	return redirect('listadoUnidad')

@login_required
def altaContacto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaContacto.html', context)

@login_required
def editaContacto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaContacto.html', context)

@login_required
def listadoContacto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoContacto.html', context)

@login_required
def altaCentroDeCosto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaCentroDeCosto.html', context)

@login_required
def editaCentroDeCosto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaCentroDeCosto.html', context)

@login_required
def listadoCentroDeCosto(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoCentroDeCosto.html', context)

@login_required
def listadoTarifario(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoTarifario.html', context)

@login_required
def exportar(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/exportar.html', context)

# devuelve AAAAMMDD
def fecha():
	import time
	return time.strftime("%Y%m%d%H%M")