from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje, persona, empresa

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    url(r'^persona/', persona, name='persona'),
    url(r'^empresa/', empresa, name='empresa'),
    #url(r'^$', 'sistema.views.index', name='index'),
]