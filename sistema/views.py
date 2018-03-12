# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
def persona(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/persona.html', context)

@login_required
def empresa(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/empresa.html', context)

@login_required
def cliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/cliente.html', context)

@login_required
def datosCliente(request):
	mensaje = ""

	context = {'mensaje': mensaje}
	return render(request, 'sistema/datosCliente.html', context)