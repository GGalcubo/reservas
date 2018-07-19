from django.conf.urls import url
from sistema.views import dashboard, operaciones, asignaciones, altaViaje, editaViaje, guardarViaje, guardarTrayecto, borrarTrayecto, altaPersona, listadoCliente, cliente, altaCliente, guardarCliente, provedor, listadoProvedor, unidad, listadoUnidad, contacto, listadoContacto, centroDeCosto, listadoCentroDeCosto, listadoTarifario, tarifario, importar_calles, eliminarCliente, exportar, guardarObservacionCliente, guardarObservacionPersona, altaUnidad, eliminarUnidad, guardarUnidad, guardarObservacionUnidad, guardarMailCliente, guardarOwnerProspect, guardarChoferProspect, licencia, listadoLicencia, guardarLicenciaUnidad, cargarLocalidad, cargarProvincia, eliminarLicenciaPropect, cargarLocalidadByProvincia, guardarCentroCostoProspect, getSelectAsignoLicencia, guardarLicencia, altaLicencia, eliminarLicencia


urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^asignaciones/', asignaciones, name='asignaciones'),
    url(r'^altaViaje/', altaViaje, name='altaViaje'),
    url(r'^editaViaje/$', editaViaje, name='editaViaje'),
    url(r'^guardarViaje/', guardarViaje, name='guardarViaje'),
    url(r'^guardarTrayecto/', guardarTrayecto, name='guardarTrayecto'),
    url(r'^borrarTrayecto/', borrarTrayecto, name='borrarTrayecto'),
    url(r'^altaPersona/', altaPersona, name='altaPersona'),
    url(r'^listadoCliente/', listadoCliente, name='listadoCliente'),
    url(r'^cliente/$', cliente, name='cliente'),
    url(r'^altaCliente/', altaCliente, name='altaCliente'),
    url(r'^guardarCliente/', guardarCliente, name='guardarCliente'),
    url(r'^eliminarCliente/', eliminarCliente, name='eliminarCliente'),
    url(r'^guardarObservacionCliente/', guardarObservacionCliente, name='guardarObservacionCliente'),
    url(r'^guardarObservacionPersona/', guardarObservacionPersona, name='guardarObservacionPersona'),
    url(r'^guardarOwnerProspect/', guardarOwnerProspect, name='guardarOwnerProspect'),
    url(r'^guardarChoferProspect/', guardarChoferProspect, name='guardarChoferProspect'),
    url(r'^guardarCentroCostoProspect/', guardarCentroCostoProspect, name='guardarCentroCostoProspect'),
    url(r'^guardarMailCliente/', guardarMailCliente, name='guardarMailCliente'),
    url(r'^provedor/', provedor, name='provedor'),
    url(r'^listadoProvedor/', listadoProvedor, name='listadoProvedor'),
    url(r'^unidad/$', unidad, name='unidad'),
    url(r'^altaUnidad/', altaUnidad, name='altaUnidad'),
    url(r'^listadoUnidad/', listadoUnidad, name='listadoUnidad'),
    url(r'^eliminarUnidad/', eliminarUnidad, name='eliminarUnidad'),
    url(r'^guardarUnidad/', guardarUnidad, name='guardarUnidad'),
    url(r'^guardarObservacionUnidad/', guardarObservacionUnidad, name='guardarObservacionUnidad'),
    url(r'^guardarLicenciaUnidad/', guardarLicenciaUnidad, name='guardarLicenciaUnidad'),
    url(r'^eliminarLicenciaPropect/', eliminarLicenciaPropect, name='eliminarLicenciaPropect'),
    url(r'^contacto/', contacto, name='contacto'),
    url(r'^listadoContacto/', listadoContacto, name='listadoContacto'),
    url(r'^centroDeCosto/', centroDeCosto, name='centroDeCosto'),
    url(r'^listadoCentroDeCosto/', listadoCentroDeCosto, name='listadoCentroDeCosto'),
    url(r'^listadoTarifario/', listadoTarifario, name='listadoTarifario'),
    url(r'^tarifario/', tarifario, name='tarifario'),
    url(r'^listadoLicencia/', listadoLicencia, name='listadoLicencia'),
    url(r'^eliminarLicencia/', eliminarLicencia, name='eliminarLicencia'),
    url(r'^licencia/', licencia, name='licencia'),
    url(r'^altaLicencia/', altaLicencia, name='altaLicencia'),
    url(r'^guardarLicencia/', guardarLicencia, name='guardarLicencia'),
    url(r'^getSelectAsignoLicencia/', getSelectAsignoLicencia, name='getSelectAsignoLicencia'),
    url(r'^cargarLocalidad/', cargarLocalidad, name='cargarLocalidad'),
    url(r'^cargarLocalidadByProvincia/', cargarLocalidadByProvincia, name='cargarLocalidadByProvincia'),
    url(r'^cargarProvincia/', cargarProvincia, name='cargarProvincia'),
    url(r'^importarcalles/', importar_calles, name='importar_calles'),
    url(r'^exportar/', exportar, name='exportar'),
    
    #url(r'^$', 'sistema.views.index', name='index'),
]