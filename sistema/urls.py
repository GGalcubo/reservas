from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje, guardarViaje, altaPersona, listadoCliente, cliente, altaCliente, guardarCliente, datosProvedor, listadoProvedor, datosUnidad, altaContacto, listadoContacto, altaCentroDeCosto, listadoCentroDeCosto, listadoTarifario, importar_calles, eliminarCliente

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    url(r'^guardarViaje/', guardarViaje, name='guardarViaje'),
    url(r'^altaPersona/', altaPersona, name='altaPersona'),
    url(r'^listadoCliente/', listadoCliente, name='listadoCliente'),
    url(r'^cliente/', cliente, name='cliente'),
    url(r'^altaCliente/', altaCliente, name='altaCliente'),
    url(r'^guardarCliente/', guardarCliente, name='guardarCliente'),
    url(r'^eliminarCliente/', eliminarCliente, name='eliminarCliente'),
    url(r'^datosProvedor/', datosProvedor, name='datosProvedor'),
    url(r'^listadoProvedor/', listadoProvedor, name='listadoProvedor'),
    url(r'^datosUnidad/', datosUnidad, name='datosUnidad'),
    url(r'^altaContacto/', altaContacto, name='altaContacto'),
    url(r'^listadoContacto/', listadoContacto, name='listadoContacto'),
    url(r'^altaCentroDeCosto/', altaCentroDeCosto, name='altaCentroDeCosto'),
    url(r'^listadoCentroDeCosto/', listadoCentroDeCosto, name='listadoCentroDeCosto'),
    url(r'^listadoTarifario/', listadoTarifario, name='listadoTarifario'),
    url(r'^importarcalles/', importar_calles, name='importar_calles'),
    
    #url(r'^$', 'sistema.views.index', name='index'),
]