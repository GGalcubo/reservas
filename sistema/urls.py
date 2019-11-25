from django.conf.urls import url

from sistema.views import *


urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^asignaciones/', asignaciones, name='asignaciones'),
    url(r'^altaViaje/', altaViaje, name='altaViaje'),
    url(r'^editaViaje/$', editaViaje, name='editaViaje'),
    url(r'^clonarViaje/', clonarViaje, name='clonarViaje'),
    url(r'^guardarViaje/', guardarViaje, name='guardarViaje'),
    url(r'^guardarViajeAdjunto/', guardarViajeAdjunto, name='guardarViajeAdjunto'),
    url(r'^guardaViajePasajeroPOST/', guardaViajePasajeroPOST, name='guardaViajePasajeroPOST'),
    url(r'^getViajesFuturosPorFecha/', getViajesFuturosPorFecha, name='getViajesFuturosPorFecha'),
    url(r'^getViajesAsignacionesPorFecha/', getViajesAsignacionesPorFecha, name='getViajesAsignacionesPorFecha'),
    url(r'^editEstadoViajeAsignaciones/', editEstadoViajeAsignaciones, name='editEstadoViajeAsignaciones'),
    url(r'^getViajePasajeros/', getViajePasajeros, name='getViajePasajeros'),
    url(r'^deleteViajeAdjunto/', deleteViajeAdjunto, name='deleteViajeAdjunto'),
    url(r'^deleteViajePasajero/', deleteViajePasajero, name='deleteViajePasajero'),
    url(r'^deleteAllViajePasajero/', deleteAllViajePasajero, name='deleteAllViajePasajero'),
    url(r'^getViajesEnProgresoPorFecha/', getViajesEnProgresoPorFecha, name='getViajesEnProgresoPorFecha'),
    url(r'^cambiarUnidadViaje/', cambiarUnidadViaje, name='cambiarUnidadViaje'),
    url(r'^mailtoViaje/', mailtoViaje, name='mailtoViaje'),
    url(r'^getDatosUnidad/', getDatosUnidad, name='getDatosUnidad'),
    url(r'^checkLocalidadFlag/', checkLocalidadFlag, name='checkLocalidadFlag'),
    url(r'^guardaViajeAdmin/', guardaViajeAdmin, name='guardaViajeAdmin'),
    url(r'^editEstadoViaje/', editEstadoViaje, name='editEstadoViaje'),
    url(r'^cambiarEstadoViajes/', cambiarEstadoViajes, name='cambiarEstadoViajes'),
    url(r'^guardarObservacionViaje/', guardarObservacionViaje, name='guardarObservacionViaje'),
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
    url(r'^guardarCentroCostoProspectDesdeViaje/', guardarCentroCostoProspectDesdeViaje, name='guardarCentroCostoProspectDesdeViaje'),
    url(r'^guardarSolicitanteProspect/', guardarSolicitanteProspect, name='guardarSolicitanteProspect'),
    url(r'^guardarPasajeroProspect/', guardarPasajeroProspect, name='guardarPasajeroProspect'),
    url(r'^guardarSolicitanteDesdeViaje/', guardarSolicitanteDesdeViaje, name='guardarSolicitanteDesdeViaje'),
    url(r'^guardarPasajeroDesdeViaje/', guardarPasajeroDesdeViaje, name='guardarPasajeroDesdeViaje'),
    url(r'^guardarMailCliente/', guardarMailCliente, name='guardarMailCliente'),
    url(r'^validarCodigoCentroCosto/', validarCodigoCentroCosto, name='validarCodigoCentroCosto'),
    url(r'^borrarSolicitanteCliente/', borrarSolicitanteCliente, name='borrarSolicitanteCliente'),
    url(r'^borrarPasajeroCliente/', borrarPasajeroCliente, name='borrarPasajeroCliente'),
    url(r'^provedor/', provedor, name='provedor'),
    url(r'^guardarProvedor/', guardarProvedor, name='guardarProvedor'),
    url(r'^altaProvedor/', altaProvedor, name='altaProvedor'),
    url(r'^getHistorial/', getHistorial, name='getHistorial'),
    url(r'^getClientes/', getClientes, name='getClientes'),
    url(r'^getClienteById/', getClienteById, name='getClienteById'),
    url(r'^getTelefonoPasajeroById/', getTelefonoPasajeroById, name='getTelefonoPasajeroById'),
    url(r'^listadoProvedor/', listadoProvedor, name='listadoProvedor'),
    url(r'^borrarProvedor/', borrarProvedor, name='borrarProvedor'),
    url(r'^unidad/$', unidad, name='unidad'),
    url(r'^unidadViaje/$', unidadViaje, name='unidadViaje'),
    url(r'^unidadDashboard/$', unidadDashboard, name='unidadDashboard'),
    url(r'^refreshUnidadDashboard/$', refreshUnidadDashboard, name='refreshUnidadDashboard'),
    url(r'^altaUnidad/', altaUnidad, name='altaUnidad'),
    url(r'^asignarIdFake/', asignarIdFake, name='asignarIdFake'),
    url(r'^listadoUnidad/', listadoUnidad, name='listadoUnidad'),
    url(r'^eliminarUnidad/', eliminarUnidad, name='eliminarUnidad'),
    url(r'^guardarUnidad/', guardarUnidad, name='guardarUnidad'),
    url(r'^guardarObservacionUnidad/', guardarObservacionUnidad, name='guardarObservacionUnidad'),
    url(r'^guardarLicenciaUnidad/', guardarLicenciaUnidad, name='guardarLicenciaUnidad'),
    url(r'^eliminarLicenciaPropect/', eliminarLicenciaPropect, name='eliminarLicenciaPropect'),
    url(r'^contacto/', contacto, name='contacto'),
    url(r'^listadoContacto/', listadoContacto, name='listadoContacto'),
    url(r'^altaCentroDeCosto/', altaCentroDeCosto, name='altaCentroDeCosto'),
    url(r'^guardarCC/', guardarCC, name='guardarCC'),
    url(r'^centroCosto/', centroCosto, name='centroCosto'),
    url(r'^listadoCentroDeCosto/', listadoCentroDeCosto, name='listadoCentroDeCosto'),
    url(r'^buscarCentroDeCostos/', buscarCentroDeCostos, name='buscarCentroDeCostos'),
    url(r'^borrarCCPropect/', borrarCCPropect, name='borrarCCPropect'),
    url(r'^listadoTarifario/', listadoTarifario, name='listadoTarifario'),
    url(r'^tarifario/', tarifario, name='tarifario'),
    url(r'^guardarTarifario/', guardarTarifario, name='guardarTarifario'),
    url(r'^editarTarifaTrayecto/', editarTarifaTrayecto, name='editarTarifaTrayecto'),
    url(r'^editarTarifaExtra/', editarTarifaExtra, name='editarTarifaExtra'),
    url(r'^guardarTarifaTrayecto/', guardarTarifaTrayecto, name='guardarTarifaTrayecto'),
    url(r'^guardarTarifaExtra/', guardarTarifaExtra, name='guardarTarifaExtra'),
    url(r'^validarTarifaTrayecto/', validarTarifaTrayecto, name='validarTarifaTrayecto'),
    url(r'^eliminarTarifaTrayecto/', eliminarTarifaTrayecto, name='eliminarTarifaTrayecto'),
    url(r'^guardarMasivo/', guardarMasivo, name='guardarMasivo'),
    url(r'^listadoLicencia/', listadoLicencia, name='listadoLicencia'),
    url(r'^eliminarLicencia/', eliminarLicencia, name='eliminarLicencia'),
    url(r'^licencia/', licencia, name='licencia'),
    url(r'^altaLicencia/', altaLicencia, name='altaLicencia'),
    url(r'^guardarLicencia/', guardarLicencia, name='guardarLicencia'),
    url(r'^getSelectAsignoLicencia/', getSelectAsignoLicencia, name='getSelectAsignoLicencia'),
    url(r'^cargarLocalidad/', cargarLocalidad, name='cargarLocalidad'),
    url(r'^cargarLocalidadByDestino/', cargarLocalidadByDestino, name='cargarLocalidadByDestino'),
    url(r'^cargarProvincia/', cargarProvincia, name='cargarProvincia'),
    url(r'^exportar/', exportar, name='exportar'),
    url(r'^exportarDatosPorCliente/', exportarDatosPorCliente, name='exportarDatosPorCliente'),
    url(r'^usuario/', usuario, name='usuario'),
    url(r'^listadoAdelanto/', listadoAdelanto, name='listadoAdelanto'),
    url(r'^adelanto/', adelanto, name='adelanto'),
    url(r'^guardarAdelanto/', guardarAdelanto, name='guardarAdelanto'),
    url(r'^altaAdelanto/', altaAdelanto, name='altaAdelanto'),
    url(r'^buscarAdelantos/', buscarAdelantos, name='buscarAdelantos'),
    url(r'^buscarViajes/', buscarViajes, name='buscarViajes'),
    url(r'^eliminarAdelanto/', eliminarAdelanto, name='eliminarAdelanto'),
    url(r'^facturarAdelantos/', facturarAdelantos, name='facturarAdelantos'),
    url(r'^listadoFactClientes/', listadoFactClientes, name='listadoFactClientes'),
    url(r'^buscarFacturacionCliente/', buscarFacturacionCliente, name='buscarFacturacionCliente'),
    url(r'^exportarPdfFactCliente/', exportarPdfFactCliente, name='exportarPdfFactCliente'),
    url(r'^exportarExcelFactCliente/', exportarExcelFactCliente, name='exportarExcelFactCliente'),
    url(r'^exportarPdfFactProv/', exportarPdfFactProv, name='exportarPdfFactProv'),
    url(r'^exportarPdfViaje/', exportarPdfViaje, name='exportarPdfViaje'),
    url(r'^buscarFacturacionProveedor/', buscarFacturacionProveedor, name='buscarFacturacionProveedor'),
    url(r'^facturarClientes/', facturarClientes, name='facturarClientes'),
    url(r'^proformarClientes/', proformarClientes, name='proformarClientes'),
    url(r'^facturarProveedores/', facturarProveedores, name='facturarProveedores'),
    url(r'^listadoFactProvedores/', listadoFactProvedores, name='listadoFactProvedores'),
    url(r'^cargarCentrosDeCosto/', cargarCentrosDeCosto, name='cargarCentrosDeCosto'),
    url(r'^cargarFactura/', cargarFactura, name='cargarFactura'),
    url(r'^cargarFacturaUnidad/', cargarFacturaUnidad, name='cargarFacturaUnidad'),
    url(r'^cargarProforma/', cargarProforma, name='cargarProforma'),
    url(r'^cargarSolicitante/', cargarSolicitantes, name='cargarSolicitantes'),
    url(r'^cargarMenu/', cargarMenu, name='cargarMenu'),
    url(r'^urlBloqueada/', urlBloqueada, name='urlBloqueada')
    #url(r'^$', 'sistema.views.index', name='index'),
]