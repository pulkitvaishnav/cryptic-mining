from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Sparse(models.Model):
	processing_time_l = models.FloatField()
	processing_time_q = models.FloatField()
	processing_time_c = models.FloatField()
	length = models.IntegerField()
