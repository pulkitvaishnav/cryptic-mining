from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Sparse(models.Model):
	processing_time = models.FloatField()
	length = models.IntegerField()
