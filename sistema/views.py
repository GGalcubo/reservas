# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calle, Localidad, Provincia, CategoriaCliente, Tarifario, Cliente, Telefono, TipoTelefono, TelefonoCliente

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
	razon_social = request.session.get('razon_social', '')
	try:
		del request.session['razon_social']
	except KeyError:
		pass
	clientes = Cliente.objects.filter(baja=False)
	if razon_social == '':
		mensajeSuccess = ''
	else:
		mensajeSuccess = 'Se dio de alta el cliente ' + razon_social
	context = {'clientes': clientes, 'mensajeSuccess':mensajeSuccess}
	return render(request, 'sistema/listadoCliente.html', context)

@login_required
def datosCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/datosCliente.html', context)

@login_required
def altaCliente(request):
	mensaje = ""
	tarifarios = Tarifario.objects.all()
	categorias = CategoriaCliente.objects.all()
	context = {'mensaje': mensaje, 'tarifarios':tarifarios, 'categorias':categorias}
	return render(request, 'sistema/altaCliente.html', context)


@login_required
def guardarCliente(request):

	cliente = Cliente()
	cliente.razon_social = request.POST.get('razonSocial', False)
	cliente.cuil = request.POST.get('cuil', False)
	cliente.direccion = request.POST.get('direccion', False)
	cliente.categoria = CategoriaCliente.objects.get(id=request.POST.get('categorias', False))
	cliente.tarifario = Tarifario.objects.get(id=request.POST.get('tarifarios', False))
	cliente.save()

	tel = Telefono()
	tel.tipo_telefono = TipoTelefono.objects.get(tipo_telefono="Principal")
	tel.numero = request.POST.get('telefono', False)
	tel.save()

	telcli = TelefonoCliente()
	telcli.cliente = cliente
	telcli.telefono = tel
	telcli.save()

	request.session['razon_social'] = cliente.razon_social

	return redirect('listadoCliente')

@login_required
def editaCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/altaCliente.html', context)

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