from django.conf.urls import url
from sistema.views import dashboard, operaciones, altaViaje, editaViaje, guardarViaje, altaPersona, listadoCliente, cliente, altaCliente, guardarCliente, provedor, listadoProvedor, unidad, listadoUnidad, altaContacto, listadoContacto, altaCentroDeCosto, listadoCentroDeCosto, listadoTarifario, importar_calles, eliminarCliente, exportar, guardarObservacionCliente, altaUnidad, eliminarUnidad, guardarUnidad

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^altaViaje/', altaViaje, name='altaViaje'),
    url(r'^editaViaje/', editaViaje, name='editaViaje'),
    url(r'^guardarViaje/', guardarViaje, name='guardarViaje'),
    url(r'^altaPersona/', altaPersona, name='altaPersona'),
    url(r'^listadoCliente/', listadoCliente, name='listadoCliente'),
    url(r'^cliente/', cliente, name='cliente'),
    url(r'^altaCliente/', altaCliente, name='altaCliente'),
    url(r'^guardarCliente/', guardarCliente, name='guardarCliente'),
    url(r'^eliminarCliente/', eliminarCliente, name='eliminarCliente'),
    url(r'^guardarObservacionCliente/', guardarObservacionCliente, name='guardarObservacionCliente'),
    url(r'^provedor/', provedor, name='provedor'),
    url(r'^listadoProvedor/', listadoProvedor, name='listadoProvedor'),
    url(r'^unidad/', unidad, name='unidad'),
    url(r'^altaUnidad/', altaUnidad, name='altaUnidad'),
    url(r'^listadoUnidad/', listadoUnidad, name='listadoUnidad'),
    url(r'^eliminarUnidad/', eliminarUnidad, name='eliminarUnidad'),
    url(r'^guardarUnidad/', guardarUnidad, name='guardarUnidad'),
    url(r'^altaContacto/', altaContacto, name='altaContacto'),
    url(r'^listadoContacto/', listadoContacto, name='listadoContacto'),
    url(r'^altaCentroDeCosto/', altaCentroDeCosto, name='altaCentroDeCosto'),
    url(r'^listadoCentroDeCosto/', listadoCentroDeCosto, name='listadoCentroDeCosto'),
    url(r'^listadoTarifario/', listadoTarifario, name='listadoTarifario'),
    url(r'^importarcalles/', importar_calles, name='importar_calles'),
    url(r'^exportar/', exportar, name='exportar'),
    
    #url(r'^$', 'sistema.views.index', name='index'),
]