from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Fibonacci(models.Model):
	fibonacci_no = models.IntegerField(unique=True)
	recursive_time = models.FloatField()
	iterative_time = models.FloatField()
	cpu_time = models.FloatField(default=0)