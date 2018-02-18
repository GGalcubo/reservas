from django.conf.urls import url
from sistema.views import dashboard

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^operaciones/', dashboard, name='operaciones'),
    #url(r'^$', 'sistema.views.index', name='index'),
]