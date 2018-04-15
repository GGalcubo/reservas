from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje, persona, empresa, cliente, datosCliente, importar_calles

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    url(r'^persona/', persona, name='persona'),
    url(r'^empresa/', empresa, name='empresa'),
    url(r'^cliente/', cliente, name='cliente'),
    url(r'^datosCliente/', datosCliente, name='datosCliente'),
    url(r'^importarcalles/', importar_calles, name='importar_calles'),
    
    #url(r'^$', 'sistema.views.index', name='index'),
]