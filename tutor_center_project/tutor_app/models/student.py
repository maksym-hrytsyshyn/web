from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    birth_date = models.DateField()
    email = models.CharField(max_length=45, unique=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=8, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
   # user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'
        managed = False
