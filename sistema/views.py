# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calle, Localidad, Provincia, CategoriaCliente, Tarifario

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
def listadoCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
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

	print request.POST['razonSocial']
	print request.POST['cuil']
	print request.POST['direccion']
	print request.POST['telefono']
	print request.POST['categorias']
	print request.POST['tarifarios']

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