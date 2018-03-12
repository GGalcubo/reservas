from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje, persona, empresa, cliente, datosCliente

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    url(r'^persona/', persona, name='persona'),
    url(r'^empresa/', empresa, name='empresa'),
    url(r'^cliente/', cliente, name='cliente'),
    url(r'^datosCliente/', datosCliente, name='datosCliente'),
    #url(r'^$', 'sistema.views.index', name='index'),
]