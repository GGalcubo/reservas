# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Estado(models.Model):
    estado = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.estado

    def __str__(self):
        return self.estado

class Viaje(models.Model):
    factura = models.CharField(max_length=30, null=True, blank=True)
    proforma = models.CharField(max_length=30, null=True, blank=True)
    estado = models.ForeignKey(Estado)
    fecha = models.CharField(max_length=8)
    hora = models.CharField(max_length=4)
    #empresa
    #vehiculo
    #observaciones
    #adjuntos
    base_total = models.IntegerField(default=0)
    peaje_total = models.IntegerField()
    estacionamiento_total = models.IntegerField()
    Otros_tot = models.IntegerField()
    maletas = models.CharField(max_length=30)
    bilingue = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.fecha

    def __str__(self):
        return self.fecha

    class Meta:
        verbose_name_plural = "Viajes" 