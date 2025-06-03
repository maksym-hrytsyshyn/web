from django.contrib.auth.models import User
from django.db import models
from .subject import Subject


class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    email = models.CharField(max_length=45, unique=True)
    phone_number = models.CharField(max_length=15)
    salary_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=55.00)

    class Meta:
        db_table = 'tutor'
        managed = False