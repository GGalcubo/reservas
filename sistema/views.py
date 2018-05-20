# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calle, Localidad, Provincia, CategoriaCliente, Tarifario, Cliente, Telefono, TipoTelefono, TelefonoCliente
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

	context = {'mensaje': mensaje}
	return render(request, 'sistema/viaje.html', context)


@login_required
def guardarViaje(request):
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
def datosProvedor(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/datosProvedor.html', context)

@login_required
def listadoProvedor(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/listadoProvedor.html', context)

@login_required
def datosUnidad(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/datosUnidad.html', context)

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