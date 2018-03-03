from django.conf.urls import url
from sistema.views import dashboard, operaciones, viaje

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', operaciones, name='operaciones'),
    url(r'^viaje/', viaje, name='viaje'),
    #url(r'^$', 'sistema.views.index', name='index'),
]