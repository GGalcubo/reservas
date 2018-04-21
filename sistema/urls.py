from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje, altaPersona, listadoCliente, datosCliente, altaCliente, altaContacto, altaCentroDeCosto, listadoCentroDeCosto, importar_calles

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    url(r'^altaPersona/', altaPersona, name='altaPersona'),
    url(r'^listadoCliente/', listadoCliente, name='listadoCliente'),
    url(r'^datosCliente/', datosCliente, name='datosCliente'),
    url(r'^altaCliente/', altaCliente, name='altaCliente'),
    url(r'^altaContacto/', altaContacto, name='altaContacto'),
    url(r'^altaCentroDeCosto/', altaCentroDeCosto, name='altaCentroDeCosto'),
    url(r'^listadoCentroDeCosto/', listadoCentroDeCosto, name='listadoCentroDeCosto'),
    url(r'^importarcalles/', importar_calles, name='importar_calles'),
    
    #url(r'^$', 'sistema.views.index', name='index'),
]